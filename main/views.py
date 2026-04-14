from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.conf import settings
from rest_framework import viewsets, filters, permissions
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer
from .models import Category, Product, Size


class IndexView(TemplateView):
    template_name = 'base.html'

class CatalogView(ListView):
    template_name = 'main/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    ordering = '-created_at'
    
    # Filtration functions for get_queryset method
    FILTER_FUNC = {
        'min_price': lambda queryset, value: queryset.filter(price__gte=value),
        'max_price': lambda queryset, value: queryset.filter(price__lte=value), 
        'color': lambda queryset, value: queryset.filter(color__iexact=value), 
        'size': lambda queryset, value: queryset.filter(product_sizes__size__name=value), 
    }
    
    SORT_FUNC = {
        'price_asc': lambda queryset: queryset.order_by('price'),
        'price_desc': lambda queryset: queryset.order_by('-price'),
        'name': lambda queryset: queryset.order_by('name')
    }
    
    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=current_category)            
        
        for params, filter_func in self.FILTER_FUNC.items():
            value = self.request.GET.get(params)
            if value:
                qs = filter_func(qs, value)
        
        for param, sort_func in self.SORT_FUNC.items():
            value = self.request.GET.get('sort')
            if value == param:
                qs = sort_func(qs)
        
        query = self.request.GET.get('q')     
        if query:
            qs = qs.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = Size.objects.all()
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(
                Category,
                slug=category_slug
            )
        
        for param in self.FILTER_FUNC.keys():
            context[param] = self.request.GET.get(param, '')
        
        context['q'] = self.request.GET.get('q', '')
                
        return context  

class ProductDetails(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['current_category'] = product.category.slug
        context['similar_products'] = Product.objects.filter(
            category=product.category).exclude(id=product.id)[:4]
        return context

class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = settings.EMAIL_HOST_USER

        return context
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ['id', 'name', 'description']
    order_fields = ['price', 'created_at']
    filterset_fields = ['category',]
    permission_classes = [IsAdminOrReadOnly, ]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]