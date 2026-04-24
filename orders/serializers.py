from rest_framework import serializers
from .models import Order, OrderItem
from main.models import Product, ProductSize, Size
from users.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['stripe_payment_intent_id']
        
class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']
        
class ProductSizeSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    class Meta:
        model = ProductSize
        fields = ['size']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    product_size = ProductSizeSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_size', 
                  'price', 'quantity']

class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user.email'
    )
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 
                  'email', 'country', 'city', 'address', 
                  'postal_code', 'order_status', 'items',
                  'payment_provider', 'payment_status',
                  'total_price', 'total_items', 
                  'created_at', 'updated_at'
                ]
        
class OrderAdminDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 
                  'email', 'country', 'city', 'address', 
                  'postal_code', 'order_status', 'items',
                  'payment_provider', 'payment_status',
                  'stripe_payment_intent_id', 'total_price', 
                  'total_items', 'created_at', 'updated_at'
                ]