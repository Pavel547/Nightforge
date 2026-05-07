from django.urls import path, include
from rest_framework import routers
from main.views import api_views

router = routers.DefaultRouter()
router.register('products', api_views.ProductViewSet, basename='products')
router.register('categories', api_views.CategoryViewSet, basename='categories')

app_name = 'main-api'

urlpatterns = [
    path('', include(router.urls))
]

