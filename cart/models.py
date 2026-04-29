from django.db import models
from main.models import Product, ProductSize
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Cart for {self.user} with session_key{self.session_key} '
    
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    
    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())
    
    
    def add_item(self, product, product_size, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            product_size=product_size,
            defaults={'quantity': quantity} 
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item
    
    
    def update_item(self, product_id, quantity):
        try: 
            item = self.items.get(id=product_id)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            return False
        
        
    def delete_item(self, product_id):
        try:
            item = self.items.get(product_id)
            item.delete()
            return True
        except CartItem.DoesNotExist:
            return False
        
    
    def clear(self):
        self.items.all().delete()

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.product.name} - {self.product_size.size.name} x {self.quantity} for {self.cart.session_key}'
    
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
