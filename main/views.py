from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Category, Product, Size


class IndexView(TemplateView):
    template_name = 'base.html'
    

class CatalogView(ListView):
    template_name = 'main/catalog.html'
    model = Product
    context_object_name = 'products'
    
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
