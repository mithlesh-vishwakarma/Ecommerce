from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        "product_name",
        "sku",
        "unit_price",
        "total_price",
    )


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0

    readonly_fields = (
        "status",
        "note",
        "changed_by",
        "created_at",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "user",
        "status",
        "payment_status",
        "subtotal",
        "discount_amount",
        "shipping_amount",
        "tax_amount",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "order_number",
        "user",
        "subtotal",
        "discount_amount",
        "shipping_amount",
        "tax_amount",
        "total_amount",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        OrderItemInline,
        OrderStatusHistoryInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product_name",
        "sku",
        "quantity",
        "unit_price",
        "total_price",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "product_name",
        "sku",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "status",
        "changed_by",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order__order_number",
    )

    readonly_fields = (
        "created_at",
    )