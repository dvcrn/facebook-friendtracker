# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from freeper import settings


class AppView(TemplateView):
    template_name = "app.html"
    additional_context = {
        'appId': settings.FACEBOOK_APP_ID
    }

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        return dict(context.items() + self.additional_context.items())