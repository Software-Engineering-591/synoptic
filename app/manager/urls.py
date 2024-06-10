from django.urls import path  # noqa: F401
from . import views  # noqa: F401

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]