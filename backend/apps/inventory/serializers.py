from rest_framework import serializers
from .models import Inventory, InventoryTransaction


# ==========================================
# INVENTORY SERIALIZER
# ==========================================
class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for tracking stock levels of product variants.
    Includes calculated read-only fields: available_quantity and is_low_stock status.
    """
    available_quantity = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "variant",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "low_stock_threshold",
            "is_low_stock",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "available_quantity",
            "is_low_stock",
            "updated_at",
        ]


# ==========================================
# INVENTORY TRANSACTION SERIALIZER
# ==========================================
class InventoryTransactionSerializer(
    serializers.ModelSerializer
):
    """
    Serializer for logging inventory stock movement (restocks, orders, adjustments).
    """
    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "variant",
            "transaction_type",
            "quantity",
            "reference",
            "note",
            "created_by",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
        ]




