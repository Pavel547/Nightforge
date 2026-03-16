import stripe
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from orders.models import Order, OrderItem
from cart.views import CartMixin
from .email import order_confirmation

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_API_KEY
stripe_webhook_key = settings.STRIPE_WEBHOOK

def create_stripe_checkout_session(order, request):
    cart = CartMixin().get_cart(request)
    line_items = []
    
    for item in cart.items.select_related('product', 'product_size__size'):
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(item.product.price * 100),
                'product_data': {
                    'name': f'{item.product.name}-{item.product_size.size.name}'
                }
            },
            'quantity': item.quantity
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=line_items,
            success_url=request.build_absolute_uri('/payment/stripe/success/')+'?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payment/stripe/cancel/')+'?session_id={CHECKOUT_SESSION_ID}',
            metadata={
                'order_id': order.id
            }
        )
        order.stripe_payment_intent_id = checkout_session.payment_intent
        order.payment_provider = 'stripe'
        order.save()
        return checkout_session
    except Exception as e:
        logger.error(f'Stripe checkout session creation error {e}')
        

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_key
        )
    except ValueError as e:
        logger.error(f'Payload value error {e}')
        return HttpResponse(status=400)
    except stripe.SignatureVerificationError as e:
        logger.error(f'Stripe signature verificateion error {e}')
        return HttpResponse(status=400)
        
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.stripe_payment_intent_id = session.get('payment_intent')
            order.order_status = 'processing'
            order.payment_status = 'paid'
            order.save()
            
            for item in order.items.all():
                size = item.product_size
                size.stock -= item.quantity
                
                if size.stock <= 0:
                    size.on_stock = False
                
                size.save()
                
            order_confirmation(request, order_id)
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found')
            return HttpResponse(status=400)
    else:
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')
        try:
            order = get_object_or_404(Order, id=order_id)
            order.payment_status = 'failed'
            order.order_status = 'cancelled'
            order.save()
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found')
            return HttpResponse(status=400)
    return HttpResponse(status=200)

def stripe_success(request):
    stripe_session_id = request.GET.get('session_id')
    if stripe_session_id:
        try:
            session = stripe.checkout.Session.retrieve(id=stripe_session_id)
            order_id = session.metadata.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            
            cart = CartMixin().get_cart(request)
            cart.clear()
            
            context = {'order': order}
            
            return render(request, 'payment/stripe/success.html', context)
        except Exception as e:
            logger.error(f'Payment success error {str(e)}')
            messages.error(request, 'Something went wrong')           
            return render(request, 'payment/stripe/success_error.html')
        
def stripe_cancel(request):
    stripe_session_id = request.GET.get('session_id')
    if stripe_session_id:
        try:
            session = stripe.checkout.Session.retrieve(id=stripe_session_id)
            order_id = session.metadata.get('order_id')
            
            order = get_object_or_404(Order, id=order_id)
            order.order_status = 'cancelled'
            order.payment_status = 'failed'
            order.save()
            
            context = {'order': order}
            
            return render(request, 'payment/stripe/cancel.html', context)
        except Exception as e:
            logger.error(f'Payment cancel error {e}')
            messages.error(request, 'Something went wrong')
            return render(request, 'payment/stripe/error.html')
