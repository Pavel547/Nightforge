from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order, OrderItem
from django.db.models import Prefetch
from smtplib import SMTPException
import logging

logger = logging.getLogger(__name__)


def order_confirmation(request, order_id):
    order = Order.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related(
                'product', 'product_size__size'
            )
        )
    ).get(id=order_id)
    
    domain = request.build_absolute_uri('/')[:-1]
    
    text_content = render_to_string(
        'email/order_confirmation.txt',
        context={'order': order}
    )
    
    html_content = render_to_string(
        'email/order_confirmation.html',
        context={'order': order, 'domain': domain}
    )
    
    try:
        msg = EmailMultiAlternatives(
            'Payment confirmation',
            text_content,
            settings.EMAIL_HOST_USER,
            [order.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        logger.info(f"Confirmation email for order {order_id} was sent")
    except SMTPException as e:
        logger.error(f"Failed to send confirmation email for order {order_id}: {e}")
    