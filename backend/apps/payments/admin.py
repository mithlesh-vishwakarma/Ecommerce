from django.contrib import admin

from .models import (
    Payment,
    PaymentTransaction,
    Refund,
)


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "payment_method",
        "amount",
        "status",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "status",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "transaction_id",
        "gateway_order_id",
    )

    readonly_fields = (
        "transaction_id",
        "gateway_order_id",
        "created_at",
        "updated_at",
    )

    inlines = [
        PaymentTransactionInline,
        RefundInline,
    ]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "transaction_id",
        "payment",
        "amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "transaction_id",
        "gateway_transaction_id",
        "payment__order__order_number",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "payment",
        "amount",
        "status",
        "gateway_refund_id",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "payment__order__order_number",
        "gateway_refund_id",
    )

    readonly_fields = (
        "gateway_refund_id",
        "created_at",
        "updated_at",
    )