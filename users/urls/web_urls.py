from django.urls import path
from users.views import web_views

app_name = 'users'

urlpatterns = [
    path('register/', web_views.register_view, name='register'),
    path('login/', web_views.login_view, name='login'),
    path('profile/', web_views.profile_view, name='profile'),
    path('edit-account-details/', web_views.edit_account_details, name='edit-account-details'),
    path('logout/', web_views.logout_view, name='logout'),
]

