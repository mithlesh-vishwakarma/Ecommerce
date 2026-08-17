from django.conf import settings
from django.db import models

# pyrefly: ignore [missing-import]
from apps.catalog.models import ProductVariant


class Inventory(models.Model):
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    quantity = models.PositiveIntegerField(default=0)

    reserved_quantity = models.PositiveIntegerField(default=0)

    low_stock_threshold = models.PositiveIntegerField(default=5)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self):
        return max(
            self.quantity - self.reserved_quantity,
            0,
        )

    @property
    def is_low_stock(self):
        return (
            self.available_quantity
            <= self.low_stock_threshold
        )

    def __str__(self):
        return f"{self.variant.sku} - {self.quantity}"


class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = (
        ("purchase", "Purchase"),
        ("sale", "Sale"),
        ("return", "Return"),
        ("damage", "Damage"),
        ("adjustment", "Adjustment"),
        ("cancellation", "Cancellation"),
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="inventory_transactions",
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPES,
    )

    quantity = models.IntegerField()

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    note = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_transactions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.sku} - {self.transaction_type}"