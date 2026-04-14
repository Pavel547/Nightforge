from django_filters.filterset import FilterSet
from django_filters import filters
from .models import Product

class ProductFilter(FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.NumberFilter(field_name='category__id')
    
    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']
