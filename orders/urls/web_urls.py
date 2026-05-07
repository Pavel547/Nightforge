from django.urls import path, include
from orders.views import web_views
from rest_framework.routers import DefaultRouter

app_name = 'orders'

urlpatterns = [
    path('checkout/', web_views.CheckoutView.as_view(), name='checkout'),
    path('user-orders/', web_views.UserOrderListView.as_view(), name='user_orders'),
    path('order/<int:pk>', web_views.OrderDetailView.as_view(), name='order'),
]
