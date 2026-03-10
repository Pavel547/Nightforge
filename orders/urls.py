from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('user-orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order')
]
