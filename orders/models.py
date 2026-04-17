from django.db import models
from django.conf import settings
from main.models import ProductSize, Product

class Order(models.Model):
    ORDER_STATUS_CHOICE = (
        ('pending_payment', 'Pending payment'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    PAYMENT_PROVIDER_CHOICE = (
        ('stripe', 'Stripe'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICE, max_length=20, 
                                    blank=True, null=True)
    payment_provider = models.CharField(choices=PAYMENT_PROVIDER_CHOICE, max_length=20,
                                        blank=True, null=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICE, max_length=20,
                                      blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=250, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order {self.email}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.name} - {self.product_size.size.name} ({self.quantity})'
    
    def total_price(self):
        return self.quantity * self.price
    