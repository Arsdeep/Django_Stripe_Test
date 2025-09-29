from django.contrib import admin
from .models import Product, Order, OrderItem

# Register Product as usual
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')


# Inline for OrderItem inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms by default
    readonly_fields = ('product', 'quantity', 'total_price')


# Register Order with the inline
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'paid', 'stripe_payment_intent', 'created_at', 'total_price')
    inlines = [OrderItemInline]
    readonly_fields = ('stripe_payment_intent', 'created_at', 'total_price')
