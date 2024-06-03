from django.shortcuts import render  # noqa: F401
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'public/home.html'

class SettingsView(TemplateView):
    template_name = 'public/settings.html'
