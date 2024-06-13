from django.urls import path  # noqa: F401
from . import views  # noqa: F401

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_water/', views.add_water_view, name='add_water'),
    path('add_sensor/', views.add_sensor_view, name='add_sensor'),
    path('', views.dashboard, name='dashboard'),
]
