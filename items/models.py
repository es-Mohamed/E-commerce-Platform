from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name")

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(
        Category, related_name='items', on_delete=models.CASCADE, verbose_name="Category"
    )
    name = models.CharField(max_length=255, verbose_name="Item Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(
        upload_to='item-image', blank=True, null=True, verbose_name="Image"
    )
    is_sold = models.BooleanField(default=False, verbose_name="Is Sold")
    created_by = models.ForeignKey(
        User, related_name="items", on_delete=models.CASCADE, verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
