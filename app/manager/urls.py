from django.urls import path  # noqa: F401
from . import views  # noqa: F401

urlpatterns = [
    path('login/', views.adminView, name='login'),
    path('hello/', views.adminView, name='hello'),
]
