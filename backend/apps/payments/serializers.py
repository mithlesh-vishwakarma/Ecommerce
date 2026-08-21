from rest_framework import serializers

from .models import (
    Payment,
    PaymentTransaction,
    Refund,
)


# ==========================================
# PAYMENT TRANSACTION SERIALIZER
# ==========================================
class PaymentTransactionSerializer(
    serializers.ModelSerializer
):
    """
    Serializer for individual payment gateway transactions (Razorpay transaction log).
    """
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


# ==========================================
# REFUND SERIALIZER
# ==========================================
class RefundSerializer(serializers.ModelSerializer):
    """
    Serializer for handling payment refund requests and tracking refund statuses.
    """
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


# ==========================================
# PAYMENT SERIALIZER
# ==========================================
class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for main Payment objects.
    Nests associated transaction history logs and refund records.
    """
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