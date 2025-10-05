from django.contrib import admin
from .models import Product, Order, OrderItem

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')


# Inline for OrderItem inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')
    can_delete = False  # Prevent deletion from inline if you want

    # Optional: show nicely in admin
    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding inline items here (optional)


# Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid', 'stripe_payment_intent', 'created_at', 'display_total_price')
    list_filter = ('paid', 'created_at', 'user')
    search_fields = ('stripe_payment_intent', 'user__username')
    readonly_fields = ('stripe_payment_intent', 'created_at', 'display_total_price')
    inlines = [OrderItemInline]

    # Display total price nicely in admin
    def display_total_price(self, obj):
        return obj.total_price()
    display_total_price.short_description = "Total Price"
