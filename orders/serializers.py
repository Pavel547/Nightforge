from rest_framework import serializers
from .models import Order, OrderItem
from users.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['stripe_payment_intent_id']
        
class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user.email'
    )
    items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=OrderItem.objects.all()
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 
                  'email', 'country', 'city', 'address', 
                  'postal_code', 'order_status', 'items',
                  'payment_provider', 'payment_status',
                  'total_price', 'total_items', 
                  'created_at', 'updated_at'
                ]