from django.db import models
from typing import TYPE_CHECKING, ClassVar, cast
from decimal import Decimal
from django.db.models.manager import Manager

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # in USD
    description = models.TextField(blank=True)
    
    # Explicit manager annotation for static type checkers
    objects: ClassVar[Manager] = models.Manager()
    
    def __str__(self):
        return self.name

class Order(models.Model):
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Explicit manager annotation for static type checkers
    objects: ClassVar[Manager] = models.Manager()

    def total_price(self) -> Decimal:
        items = self.items.all()  # type: ignore[attr-defined]
        return sum((item.total_price() for item in items), Decimal("0"))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    # Explicit manager annotation for static type checkers
    objects: ClassVar[Manager] = models.Manager()

    def total_price(self) -> Decimal:
        product = cast(Product, self.product)
        quantity_val: int = cast(int, self.quantity)
        price_dec = cast(Decimal, product.price)
        return Decimal(quantity_val) * price_dec
