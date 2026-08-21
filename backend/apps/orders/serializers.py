from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
)


# ==========================================
# ORDER ITEM SERIALIZER
# ==========================================
class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual items captured at the time of order placement.
    Includes item snapshot details (product name, unit price, quantity, total price).
    """
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "variant",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "product_name",
            "sku",
            "unit_price",
            "total_price",
            "created_at",
        ]


# ==========================================
# ORDER STATUS HISTORY SERIALIZER
# ==========================================
class OrderStatusHistorySerializer(
    serializers.ModelSerializer
):
    """
    Serializer for tracking order status transitions (e.g. Pending -> Confirmed -> Shipped).
    Computes full name of user who made the status update.
    """
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatusHistory
        fields = [
            "id",
            "status",
            "note",
            "changed_by",
            "changed_by_name",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "changed_by",
            "changed_by_name",
            "created_at",
        ]

    def get_changed_by_name(self, obj):
        """
        Returns string full name of staff or user modifying status.
        """
        if obj.changed_by:
            return obj.changed_by.get_full_name()

        return None


# ==========================================
# ORDER SERIALIZER
# ==========================================
class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for full Order objects.
    Nests order items and status audit history.
    """
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    status_history = OrderStatusHistorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "order_number",
            "user",
            "status",
            "payment_status",
            "subtotal",
            "discount_amount",
            "shipping_amount",
            "tax_amount",
            "total_amount",
            "shipping_address",
            "billing_address",
            "notes",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "order_number",
            "user",
            "status",
            "payment_status",
            "subtotal",
            "discount_amount",
            "shipping_amount",
            "tax_amount",
            "total_amount",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        ]


# ==========================================
# CHECKOUT SERIALIZER
# ==========================================
class CheckoutSerializer(serializers.Serializer):
    """
    Serializer for validating incoming checkout request payloads.
    Requires shipping address ID and optional billing address ID or customer notes.
    """
    shipping_address_id = serializers.IntegerField()

    billing_address_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )