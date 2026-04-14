from django.urls import path
from .views import API_Register

urlpatterns = [
    path('register/', API_Register.as_view(), name='api-register')
]