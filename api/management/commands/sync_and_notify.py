import json
import urllib2

from django.core.management.base import NoArgsCommand
from api.models import Person
from api.helper import add_entry_to_history, compare_dictionaries
from freeper import settings


class Command(NoArgsCommand):
    help = "Calculates app differences and publishes notifications"

    def handle(self, *args, **options):
        persons = Person.objects.all()
        for person in persons:
            print person.facebook_id

            endpoint_url = 'https://graph.facebook.com/me/friends/?access_token=%s' % person.access_token
            response = urllib2.urlopen(endpoint_url)
            json_parsed_response = json.loads(response.read())

            existing_friendlist = person.friends

            # Parse multi level friends dict into single level dict
            new_friendlist = {}
            for friend in json_parsed_response['data']:
                new_friendlist[friend['id']] = friend['name']

            differences = compare_dictionaries(existing_friendlist, new_friendlist)

            # Merge new and old losts and put them back into the model
            person.lost_friends = dict(differences['removed_entries'].items() + person.lost_friends.items())
            person.new_friends = dict(differences['added_entries'].items() + person.new_friends.items())

            # Generate a notification message
            removed_entries_length = len(differences['removed_entries'])
            if removed_entries_length > 0:
                notification_template = '%s disappeared from your friendlist.' % differences['removed_entries'].itervalues().next()
                ref = 'notif_removed'
                if removed_entries_length > 1:
                    notification_template = '%s and %d other(s) disappeared from your friendlist.' % (
                        differences['removed_entries'].itervalues().next(), (removed_entries_length - -1))

            # Only show the 'xxxx is new' message when there is no deleted entry
            added_entries_length = len(differences['added_entries'])
            if added_entries_length > 0 and removed_entries_length == 0:
                notification_template = '%s is new in your friendlist.' % differences['added_entries'].itervalues().next()
                ref = 'notif_added'
                if added_entries_length > 1:
                    notification_template = '%s and %d other(s) are new in your friendlist.' % (
                        differences['added_entries'].itervalues().next(), (added_entries_length - 1))

            if len(differences['added_entries']) > 0 or len(differences['removed_entries']) > 0:
                history = person.history
                add_entry_to_history(history, len(new_friendlist))

                person.history = history
                person.friends = new_friendlist

                person.save()

                # Publish the message to facebook
                notification_endpoint = 'https://graph.facebook.com/%s/notifications/' % person.facebook_id
                urllib2.urlopen(notification_endpoint, 'access_token=%s|%s&template=%s&ref=%s' % (settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, notification_template, ref))
