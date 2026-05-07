from django.urls import path
from users.views import api_views

app_name = 'users_api'

urlpatterns = [
    path('register/', api_views.API_Register.as_view(), name='api-register'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='api-profile')
]