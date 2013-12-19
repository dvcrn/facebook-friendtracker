# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse


class AppView(TemplateView):
    template_name = "app.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)