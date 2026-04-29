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
        read_only = True
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
        extra_kwargs = {
            'id': {'read_only': True},
            'total_price': {'read_only':True},
            'total_items': {'read_only': True},
        }
        
class OrderAdminDetailSerializer(OrderDetailSerializer):
    class Meta(OrderDetailSerializer.Meta):
        fields = OrderDetailSerializer.Meta.fields + ['stripe_payment_intent_id']
    
    def validate_postal_code(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('Invalid postal code')
        return value
    