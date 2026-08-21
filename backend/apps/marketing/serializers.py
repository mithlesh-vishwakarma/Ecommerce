from rest_framework import serializers

from .models import Coupon, CouponUsage


# ==========================================
# COUPON SERIALIZER
# ==========================================
class CouponSerializer(serializers.ModelSerializer):
    """
    Serializer for managing discount coupons, validity dates, minimum order limits, and usage counts.
    """
    class Meta:
        model = Coupon

        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "minimum_order_value",
            "maximum_discount",
            "usage_limit",
            "used_count",
            "starts_at",
            "expires_at",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "used_count",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "code": {
                "validators": [],
            }
        }

    def validate_code(self, value):
        """
        Normalizes coupon codes to uppercase and strips whitespace.
        """
        return value.strip().upper()


# ==========================================
# COUPON USAGE SERIALIZER
# ==========================================
class CouponUsageSerializer(
    serializers.ModelSerializer
):
    """
    Serializer for tracking coupon redemption records per user and order.
    """
    class Meta:
        model = CouponUsage

        fields = [
            "id",
            "coupon",
            "user",
            "order",
            "discount_amount",
            "used_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "order",
            "discount_amount",
            "used_at",
        ]


