from django.urls import path  # noqa: F401
from . import views  # noqa: F401

urlpatterns = [
    path('login/', views.admin_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_sensor_view, name="add_sensor"),  
    path('', views.dashboard, name='dashboard'),
]
  
