from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, OrderItem

class OrderItemilnline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('preview_image', 'product', 'product_size', 'price', 'quantity',
              'total_price')
    readonly_fields = ('preview_image', 'total_price')
    can_delete = False
    
    def preview_image(self, obj):
        if obj.product.main_image:
            return mark_safe(f"""<img src="{obj.product.main_image.url}" 
                             style="max-height:100px; max-width:100px; object-fit: cover;"/>""")
        else:
            return mark_safe("""<span style="color:gray">Image not found</span>""")
    preview_image.short_description = 'Preview image'
    
    
    def total_price(self, obj):
        try:
            return obj.total_price()
        except TypeError:
            return mark_safe("""<span style="color:red;">Invalid data</span>""")
    total_price.short_description = 'Total price'
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email','first_name', 'last_name',
                    'country', 'order_status', 'payment_provider', 
                    'total_price', 'total_items','created_at', 'updated_at', )
    list_filter = ('payment_provider', 'country', 'order_status')
    search_fields = ('email', 'first_name', 'lust_name')
    readonly_fields = ('total_price', 'created_at', 'updated_at',
                       'stripe_payment_intent_id', 'total_items')
    date_hierarchy = 'created_at'
    inlines = (OrderItemilnline, )
    fieldsets = (
        ('Order data', {
            "fields": (
                'user', 'first_name', 'last_name', 'email',
                'order_status', 'payment_status',
                'created_at', 'updated_at'
            ),
        }),
        ('Delivery data', {
            'fields': (
                'country', 'city', 'address', 'postal_code'
            ),
        }),
        ('Paymant data', {
            'fields': (
                'payment_provider', 'stripe_payment_intent_id',
                'total_price', 'total_items',
            )
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj) or ()
        
        if obj:
            return readonly + (
                'user', 'email', 'first_name', 'last_name',
                'country', 'city', 'address', 'postal_code',
            )
        return readonly
            
