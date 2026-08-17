from rest_framework import serializers

from .models import (
    Payment,
    PaymentTransaction,
    Refund,
)


class PaymentTransactionSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "transaction_id",
            "gateway_transaction_id",
            "amount",
            "status",
            "gateway_response",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = [
            "id",
            "payment",
            "amount",
            "reason",
            "gateway_refund_id",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "gateway_refund_id",
            "status",
            "created_at",
            "updated_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    transactions = PaymentTransactionSerializer(
        many=True,
        read_only=True,
    )

    refunds = RefundSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "payment_method",
            "transaction_id",
            "gateway_order_id",
            "amount",
            "status",
            "paid_at",
            "transactions",
            "refunds",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "transaction_id",
            "gateway_order_id",
            "amount",
            "status",
            "paid_at",
            "transactions",
            "refunds",
            "created_at",
            "updated_at",
        ]