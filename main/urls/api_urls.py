from django.urls import path, include
from rest_framework import routers
from main.views import api_views

app_name = 'main_api'

router = routers.DefaultRouter()
router.register('products', api_views.ProductViewSet, basename='products')
router.register('categories', api_views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]

