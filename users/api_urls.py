from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.API_Register.as_view(), name='api-register'),
    path('profile/', views.ProfileAPIView.as_view(), name='api-profile')
]