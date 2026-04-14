from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'main'

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog_all'),
    path('catalog/<slug:category_slug>', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>', views.ProductDetails.as_view(), name='product'),
    path('contact-us/', views.ContactView.as_view(), name='contact_us'),
    path('', include(router.urls)),
]

