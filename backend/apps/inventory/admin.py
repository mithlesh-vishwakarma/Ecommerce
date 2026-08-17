from django.contrib import admin

from .models import (
    Inventory,
    InventoryTransaction,
)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variant",
        "quantity",
        "reserved_quantity",
        "available_stock",
        "low_stock",
        "updated_at",
    )

    list_filter = (
        "variant__product",
    )

    search_fields = (
        "variant__sku",
        "variant__product__name",
    )

    readonly_fields = (
        "updated_at",
    )

    @admin.display(description="Available Stock")
    def available_stock(self, obj):
        return obj.available_quantity

    @admin.display(
        boolean=True,
        description="Low Stock",
    )
    def low_stock(self, obj):
        return obj.is_low_stock


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variant",
        "transaction_type",
        "quantity",
        "reference",
        "created_by",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    search_fields = (
        "variant__sku",
        "variant__product__name",
        "reference",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )