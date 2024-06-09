from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('alert/', views.AlertView.as_view()),
    path('settings', views.SettingsView.as_view()),
]
