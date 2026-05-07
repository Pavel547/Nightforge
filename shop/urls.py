from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main/', include('main.urls.api_urls', namespace='main_api')),
    path('api/orders/', include('orders.urls.api_urls', namespace='orders_api')),
    path('api-auth/', include('rest_framework.urls', namespace='api_auth')),
    path('api/users/', include('users.urls.api_urls', namespace='users_api')),
    path('', include('main.urls.web_urls', namespace='main')),
    path('users/', include('users.urls.web_urls', namespace='users')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('orders.urls.web_urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment'))
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
