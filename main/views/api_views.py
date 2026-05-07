from rest_framework import viewsets, permissions, filters
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from main.models import Product, ProductSize, Category
from main.serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer
from main.permissions import IsAdminOrReadOnly
from main.filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    ps_queryset = ProductSize.objects.select_related(
        'size'
    )
    queryset = Product.objects.select_related(
        'category'
    ).prefetch_related(Prefetch(
        'product_sizes',
        queryset=ps_queryset
    ))
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ['id', 'name', 'description']
    ordering_fields = ['price', 'created_at']
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]