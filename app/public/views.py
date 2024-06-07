from django.shortcuts import render  # noqa: F401
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
# Create your views here.


class HomeView(TemplateView):
    template_name = 'public/home.html'
