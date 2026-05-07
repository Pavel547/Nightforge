from django.urls import path, include
from rest_framework import routers
from orders.views import api_views

app_name = 'orders_api'

router = routers.DefaultRouter()
router.register('orders', api_views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]
