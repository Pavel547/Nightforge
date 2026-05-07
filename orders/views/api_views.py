from rest_framework import mixins, viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Order, OrderItem
from django.db.models import Prefetch
from orders.filters import CustomSearchFilter
from orders import serializers

class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    
    permission_classes = [
        permissions.IsAuthenticated, 
    ]
    filter_backends = [
        CustomSearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    ordering_fields = ['created_at', 'updated_at', 
                       'total_price']
    ordering = ['-created_at']
    search_fields = ['email', 'id']
    filterset_fields = ['order_status', 'payment_provider', 
                        'payment_status']
    
    def get_queryset(self):
        base_qs = Order.objects.select_related('user').prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related(
                    'product', 'product_size__size'
                )
            )
        )
        if self.request.user.is_staff:
            return base_qs
        return base_qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdminOrderSerializer if self.request.user.is_staff else serializers.OrderSerializer
        
        if self.action == 'retrieve':
            return serializers.OrderAdminDetailSerializer if self.request.user.is_staff else serializers.OrderDetailSerializer
        
        return serializers.OrderSerializer