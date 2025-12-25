from django.db import models
from django.contrib.auth.models import User
from items.models import Item

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Carts'

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Anonymous Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'item')

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Cart {self.cart.id}"

    @property
    def total_price(self):
        return self.quantity * self.price_at_addition

