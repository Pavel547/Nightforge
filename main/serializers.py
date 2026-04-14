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

class ProductDetailSizeSerializer(serializers.ModelSerializer):
    size = SizeDetailSerializer()

    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'stock']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }
        
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_sizes = ProductDetailSizeSerializer(many=True, required=False)
    category = CategoryDetailSerializer(read_only=True)
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
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
    def create(self, validated_data):
        product_sizes = validated_data.pop('product_sizes')
        product = Product.objects.create(**validated_data)
        
        for product_size in product_sizes:
            size, _ = Size.objects.get_or_create(name=product_size['size']['name'])
            ProductSize.objects.create(product=product, size=size, stock=product_size['stock'])
        return product
    
    def update(self, instance, validated_data):
        product_sizes = validated_data.pop('product_sizes', None)
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.color = validated_data.get('color', instance.color)
        instance.description = validated_data.get('description', instance.description)
        instance.main_image = validated_data.get('main_image', instance.main_image)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        
        if product_sizes is not None:
            for size_data in product_sizes:
                size, _ = Size.objects.get_or_create(name=size_data['size']['name'])
                product_size_id = size_data.get('id')
                if product_size_id:
                    ps = ProductSize.objects.get(id=product_size_id, product=instance)
                    ps.size.name = size_data.get('size', {}).get('name', ps.size.name)
                    ps.stock = size_data.get('stock', ps.stock)
                    ps.save()
                else:
                    ProductSize.objects.get_or_create(product=instance, size=size, defaults={'stock': size_data['stock']})
        return instance