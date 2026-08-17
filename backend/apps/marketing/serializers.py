from rest_framework import serializers

from .models import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
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
        return value.strip().upper()


class CouponUsageSerializer(
    serializers.ModelSerializer
):
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

