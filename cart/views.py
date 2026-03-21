from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.template.response import TemplateResponse
from .models import Cart, CartItem
from .forms import UpdateCartItem, AddToCartForm
from main.models import Product, ProductSize
from django.db import transaction
import json


class CartMixin:
# Get user cart method
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=request.user
            )
            return cart
        else:
            if not request.session.session_key:
                request.session.create()
                
            cart, created = Cart.objects.get_or_create(
                session_key=request.session.session_key,
            )
            return cart

# Merg old and new carts method
    def merge_carts(self, request, old_session):
        if old_session:
            old_cart = Cart.objects.filter(
                session_key=old_session,
                user__isnull=True
            ).first()
            
            if old_cart:
                new_cart, created = Cart.objects.get_or_create(
                    user=request.user
                )
                
                for item in old_cart.items.all():
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=new_cart,
                        product=item.product,
                        product_size=item.product_size,
                        defaults={'quantity': item.quantity}
                    )
                    
                    if not created:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    
                old_cart.delete()
                        
class CartDetailView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'product', 'product_size__size').order_by('-added_at')
        }
        
        return TemplateResponse(request, 'cart/cart.html', context)
    

class AddToCartView(CartMixin, View):
    @transaction.atomic
    def post(self, request, slug):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, slug=slug)
        
        form = AddToCartForm(request.POST, product=product)
        
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('main:product', product.slug)

        size_id = form.cleaned_data.get('size_id')
        quantity = form.cleaned_data.get('quantity', 1)
        
        
        product_size = get_object_or_404(ProductSize, product=product, id=size_id)
        
        if quantity > product_size.stock:
            messages.info(request,
                          f'Only {product_size.stock} pieces avalible now')
            return redirect('main:product', product.slug)
            
        existing_item = cart.items.filter(product=product, product_size=product_size).first()
        if existing_item:
            total_quantity = existing_item.quantity + quantity
            if total_quantity > product_size.stock:
                message = f"""Cannot add {quantity} items. 
                Only {product_size.stock - existing_item.quantity} more available."""
                messages.info(request, message=message)
                return redirect('main:product', product.slug)
                
        cart_item = cart.add_item(product, product_size, quantity)
        
        messages.success(request, f'{product.name} succesfully add to cart')
        
        return redirect('main:product', product.slug)
        
    
class UpdateCartItemView(CartMixin, View):
    @transaction.atomic
    def post(self, request, item_id):
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        
        quantity = int(request.POST.get('quantity'))
        
        if quantity < 0:
            messages.error(request, 'Invalid quantity')
            return redirect('cart:details')
            
        if quantity == 0:
            cart_item.delete()
            return redirect('cart:details')
        else:
            if quantity > cart_item.product_size.stock:
                messages.error(request, 
                               f'Only {cart_item.product_size.stock} avalible now')
                return redirect('cart:details')
            cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart:details')


class DeleteCartItemView(CartMixin, View):
    def post(self, request, item_id):
        cart = self.get_cart(request)
        
        try:
            cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
            cart_item.delete()
            
            return redirect('cart:details')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found')
            

class ClearCartView(CartMixin, View):
    def post(self, request):
        cart = self.get_cart(request)
        cart.clear()
        
        messages.info(request, 'Cart successfully cleared')
        return redirect('cart:details')
    
