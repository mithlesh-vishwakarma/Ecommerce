from rest_framework import serializers
from .models import Inventory, InventoryTransaction

class InventorySerializer(serializers.ModelSerializer):
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


class InventoryTransactionSerializer(
    serializers.ModelSerializer
):
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



