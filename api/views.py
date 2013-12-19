from django.views.generic import View
from django.http import HttpResponse
from api.models import Person
from api.helper import compare_dictionaries, add_entry_to_history
from freeper import settings
import json
import urllib2
import time
import datetime


class FacebookApiView(View):
    access_token = ''

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.access_token = request.POST.get('access_token', None)
            if not self.access_token:
                try:
                    payload = json.loads(request.body)
                    self.access_token = payload['access_token']
                except Exception:
                    pass

        if request.method == 'GET':
            self.access_token = request.GET.get('access_token', '')

        return super(FacebookApiView, self).dispatch(request, *args, **kwargs)

    def do_graph_request(self, endpoint):
        response = urllib2.urlopen('https://graph.facebook.com/%s/?access_token=%s'
                                   % (endpoint, self.access_token))
        return json.loads(response.read())

    def exchange_long_lived_access_token(self):
        url = 'https://graph.facebook.com/oauth/access_token?' \
              'grant_type=fb_exchange_token' \
              '&client_id=%s' \
              '&client_secret=%s' \
              '&fb_exchange_token=%s' % (settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, self.access_token)

        response = urllib2.urlopen(url)

        data = {}
        payload = response.read()  # format access_token=xxxx&expires=123
        payload = payload.split('&')
        for group in payload:
            key_value = group.split('=')  # [access_token, xxxx]
            data[key_value[0]] = key_value[1]

        return data

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)


class SaveApiView(FacebookApiView):
    def post(self, request, *args, **kwargs):
        user_data = self.do_graph_request('me')
        user_friends = self.do_graph_request('me/friends')['data']
        ll_access_token_data = self.exchange_long_lived_access_token()

        # Parse multi level friends dict into single level dict
        friend_list = {}
        for friend in user_friends:
            friend_list[friend['id']] = friend['name']

        history = {}
        existing_friend_list = {}
        existing_new_friend_list = {}
        existing_lost_friend_list = {}

        try:
            user = Person.objects.get(facebook_id=user_data['id'])
            history = user.history
            existing_friend_list = user.friends
            existing_lost_friend_list = user.lost_friends
            existing_new_friend_list = user.new_friends
        except Person.DoesNotExist:
            user = Person(facebook_id=user_data['id'])

        # Save long lived access token
        now = datetime.datetime.now()
        token_expires = now + datetime.timedelta(seconds=int(ll_access_token_data['expires']))

        user.access_token = ll_access_token_data['access_token']
        user.access_token_expires_at = token_expires

        if existing_friend_list:
            compare_result = compare_dictionaries(existing_friend_list, friend_list)

            # Merge new and old losts and put them back into the model
            user.lost_friends = dict(compare_result['removed_entries'].items() + existing_lost_friend_list.items())
            user.new_friends = dict(compare_result['added_entries'].items() + existing_new_friend_list.items())

        add_entry_to_history(history, len(friend_list))

        user.friends = friend_list
        user.history = history
        user.save()

        return HttpResponse(status=200, content=json.dumps({'new_friends': user.new_friends,
                                                            'lost_friends': user.lost_friends,
                                                            'history': user.history}),
                            content_type='application/json')


class ResetApiView(FacebookApiView):
    def post(self, request, *args, **kwargs):
        user_data = self.do_graph_request('me')
        try:
            user = Person.objects.get(facebook_id=user_data['id'])
            user.lost_friends = {}
            user.new_friends = {}
            user.save()

            return HttpResponse(status=200)

        except Person.DoesNotExist:
            return HttpResponse(status=404)