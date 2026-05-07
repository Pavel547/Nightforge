from django.urls import path
from main.views import web_views

app_name = 'main'

urlpatterns = [
    path('', web_views.IndexView.as_view(), name='index'),
    path('catalog/', web_views.CatalogView.as_view(), name='catalog_all'),
    path('catalog/<slug:category_slug>', web_views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>', web_views.ProductDetails.as_view(), name='product'),
    path('contact-us/', web_views.ContactView.as_view(), name='contact_us'),
]

