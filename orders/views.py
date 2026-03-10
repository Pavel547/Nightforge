from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Prefetch
from cart.views import CartMixin
from .forms import OrderForm
from .models import Order, OrderItem
from decimal import Decimal
from payment.views import create_stripe_checkout_session
import logging

logger = logging.getLogger(__name__)

@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class CheckoutView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        
        if cart.total_items == 0:
            logger.warning('Cart is empty redirect to cart page')
            return redirect('cart:details')
        
        form = OrderForm(user=request.user)
        
        context = {
            'cart': cart,
            'cart_total_price': cart.subtotal,
            'cart_items': cart.items.select_related(
                'product', 'product_size__size'
            ).order_by('-added_at'),
            'form': form
        }
        
        return render(request, 'orders/checkout.html', context)
    
    def post(self, request):
        cart = self.get_cart(request)
        payment_provider = request.POST.get('payment_provider')
        
        if cart.total_items == 0:
            logger.warning('Cart is empty redirect to cart page')
            return redirect('cart:details')
        
        if not payment_provider or payment_provider != 'stripe': #For more payment providers use not in [some payment provider]
            logger.warning('Invalid or missing payment provider')
            
            context = {
                'cart': cart,
                'cart_total_price': cart.subtotal,
                'cart_items': cart.items.select_related(
                    'product', 'product_size__size'
                ).order_by('-added_at'),
                'form': OrderForm(user=request.user)
            }
            
            return render(request, 'orders/checkout.html', context)
        
        form_data = request.POST.copy()
        cart_total_price = cart.subtotal
        cart_total_items = cart.total_items
        if not form_data.get('email'):
            form_data['email'] = request.user.email
            
        form = OrderForm(form_data, user=request.user)
        
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                country=form.cleaned_data['country'],
                city=form.cleaned_data['city'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                order_status='pending_payment',
                payment_status='pending',
                payment_provider=payment_provider,
                total_price=cart_total_price,
                total_items=cart_total_items
            )
            
            for item in cart.items.select_related('product', 'product_size'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_size=item.product_size,
                    quantity=item.quantity,
                    price=item.product.price or Decimal('0.00')
                )
            try:
                if payment_provider == 'stripe':
                    logger.debug(f'Create stripe checkout session for {order.id}')
                    checkout_session = create_stripe_checkout_session(order, request)
                    
                    return redirect(checkout_session.url)
            except Exception as e:
                logger.error(f'Payment creating error {str(e)}', exc_info=True)
                context = {
                    'cart': cart,
                    'form': form,
                    'cart_items': cart.items.select_related(
                        'product', 'product_size__size'
                    ).order_by('-added_at'),
                    'cart_total_price': cart.subtotal, 
                }
                messages.error(request, f'Payment processing error {e}')
                return render(request, 'orders/checkout.html', context)
        else:
            logger.error('Form validation error')
            order.delete()
            context = {
                'cart': cart,
                'form': form,
                'cart_items': cart.items.select_related(
                    'product', 'product_size__size'
                ).order_by('-added_at'),
                'cart_total_price': cart.subtotal
            }
            return render(request, 'orders/checkout.html', context)

class UserOrderListView(ListView):
    model = Order
    template_name = 'orders/user_orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user).order_by('-updated_at')

        return qs
    
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(Prefetch(
            'items', 
            queryset=OrderItem.objects.select_related(
                'product', 'product_size__size')))

        return qs
