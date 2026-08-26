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

    actions = ["process_full_refund", "mark_as_failed_and_release_stock"]

    @admin.action(description="Process Full Refund for selected payments")
    def process_full_refund(self, request, queryset):
        from .services import process_refund
        success_count = 0
        for payment in queryset:
            if payment.status == Payment.Status.SUCCESS:
                try:
                    process_refund(
                        payment=payment,
                        amount=payment.amount,
                        reason="Admin bulk full refund.",
                        user=request.user,
                    )
                    success_count += 1
                except Exception as e:
                    self.message_user(request, f"Error refunding payment {payment.id}: {e}", level="ERROR")
        self.message_user(request, f"Successfully processed refund for {success_count} payment(s).")

    @admin.action(description="Mark as FAILED and release reserved stock")
    def mark_as_failed_and_release_stock(self, request, queryset):
        from .services import handle_payment_failure
        count = 0
        for payment in queryset:
            if payment.status != Payment.Status.SUCCESS:
                handle_payment_failure(payment, reason="Admin marked as failed.", user=request.user)
                count += 1
        self.message_user(request, f"Successfully failed and released stock for {count} payment(s).")



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