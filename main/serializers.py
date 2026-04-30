from rest_framework import serializers
from .models import Category, ProductSize, Product, Size

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    product_sizes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ProductSize.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    class Meta:
        model = Product
        fields =['id', 'name', 'product_sizes', 'category', 
                 'description', 'main_image', 'color', 
                 'price', 'created_at', 'updated_at']

class SizeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []}
        }

class ProductSizeDetailSerializer(serializers.ModelSerializer):
    size = SizeDetailSerializer()

    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'stock']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

class ProductDetailSerializer(serializers.ModelSerializer):
    product_sizes = ProductSizeDetailSerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        write_only=True,
        source='category',
    )
    main_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_id','product_sizes', 
                  'description', 'main_image', 'color', 'price', 'created_at', 
                  'updated_at']
        extra_kwargs = {
            'id':{'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
    def create(self, validated_data):
        product_sizes = validated_data.pop('product_sizes', [])
        product = Product.objects.create(**validated_data)
        
        for product_size in product_sizes:
            size, _ = Size.objects.get_or_create(name=product_size['size']['name'])
            ProductSize.objects.create(product=product, size=size, stock=product_size['stock'])
        return product
    
    def update(self, instance, validated_data):
        product_sizes = validated_data.pop('product_sizes', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if product_sizes is not None:
            for size_data in product_sizes:
                size, _ = Size.objects.get_or_create(name=size_data['size']['name'])
                product_size_id = size_data.get('id')
                if product_size_id:
                    try:
                        ps = ProductSize.objects.get(id=product_size_id, product=instance)
                        ps.size.name = size_data.get('size', {}).get('name', ps.size.name)
                        ps.stock = size_data.get('stock', ps.stock)
                        ps.save()
                    except ProductSize.DoesNotExist:
                        raise serializers.ValidationError(
                            f'product_size with id {product_size_id} not found'
                        )
                else:
                    ProductSize.objects.get_or_create(product=instance, size=size, defaults={'stock': size_data['stock']})
        return instance
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Invalid price')
        return value
    
    def validate_product_sizes(self, value):
        for items in value:
            if items['stock'] < 0:
                raise serializers.ValidationError('Invalid stock number')
        return value
    