from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
)


class OrderItemSerializer(serializers.ModelSerializer):
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


class OrderStatusHistorySerializer(
    serializers.ModelSerializer
):
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
        if obj.changed_by:
            return obj.changed_by.get_full_name()

        return None


class OrderSerializer(serializers.ModelSerializer):
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


class CheckoutSerializer(serializers.Serializer):

    shipping_address_id = serializers.IntegerField()

    billing_address_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )