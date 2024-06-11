from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('weather/', views.WeatherView.as_view()),
    path('alert/', views.AlertView.as_view()),
    path('settings', views.SettingsView.as_view()),
    path(
        'daily_weather/',
        views.PartialDailyWeatherView.as_view(),
        name='daily_weather',
    ),
    path(
        'weekly_weather/',
        views.PartialWeeklyWeatherView.as_view(),
        name='weekly_weather',
    ),
]
