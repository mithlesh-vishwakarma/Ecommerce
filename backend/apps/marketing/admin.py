from django.contrib import admin

from .models import (
    Coupon,
    CouponUsage,
)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
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
    )

    list_filter = (
        "discount_type",
        "is_active",
        "starts_at",
        "expires_at",
    )

    search_fields = (
        "code",
    )

    readonly_fields = (
        "used_count",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "coupon",
        "user",
        "order",
        "discount_amount",
        "used_at",
    )

    list_filter = (
        "used_at",
    )

    search_fields = (
        "coupon__code",
        "user__username",
        "user__email",
        "order__order_number",
    )

    readonly_fields = (
        "used_at",
    )