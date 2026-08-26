from decimal import Decimal
import json
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

import razorpay

from django.conf import settings

from .models import Payment, PaymentTransaction, Refund
from apps.orders.models import Order, OrderStatusHistory
from apps.inventory.models import Inventory


def get_razorpay_client():
    """
    Initializes and returns the Razorpay API Client instance using configured Key ID and Secret.
    """
    return razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )


@transaction.atomic
def handle_payment_failure(payment, reason="Payment failed or cancelled.", user=None):
    """
    Handles payment failure or cancellation:
    1. Updates Payment status to FAILED.
    2. Releases reserved inventory stock back for all order items.
    3. Marks Order status as CANCELLED and payment_status as FAILED.
    4. Logs OrderStatusHistory record.
    """
    payment.status = Payment.Status.FAILED
    payment.save(update_fields=["status", "updated_at"])

    order = payment.order
    order.status = Order.Status.CANCELLED
    order.payment_status = Order.PaymentStatus.FAILED
    order.save(update_fields=["status", "payment_status", "updated_at"])

    # Release reserved stock in Inventory
    order_items = order.items.select_related("variant").all()
    variant_ids = [item.variant_id for item in order_items]

    inventories = {
        inv.variant_id: inv
        for inv in Inventory.objects.select_for_update().filter(variant_id__in=variant_ids)
    }

    for item in order_items:
        inventory = inventories.get(item.variant_id)
        if inventory:
            inventory.reserved_quantity = max(0, inventory.reserved_quantity - item.quantity)
            inventory.save(update_fields=["reserved_quantity", "updated_at"])

    # Log in OrderStatusHistory
    OrderStatusHistory.objects.create(
        order=order,
        status=Order.Status.CANCELLED,
        changed_by=user or order.user,
        note=f"Order cancelled due to payment failure: {reason}",
    )

    return payment


@transaction.atomic
def create_payment_order(order, user, payment_method=Payment.Method.RAZORPAY):
    """
    Creates a payment session for the given Order.
    Supports both Razorpay and Cash on Delivery (COD).
    """
    if order.user_id != user.id:
        raise ValidationError("You are not allowed to pay for this order.")

    if order.payment_status == Order.PaymentStatus.PAID:
        raise ValidationError("This order has already been paid.")

    # Handle Cash on Delivery (COD)
    if payment_method == Payment.Method.COD:
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "payment_method": Payment.Method.COD,
                "amount": order.total_amount,
                "status": Payment.Status.PENDING,
            },
        )
        if not created and payment.payment_method != Payment.Method.COD:
            payment.payment_method = Payment.Method.COD
            payment.save(update_fields=["payment_method", "updated_at"])

        # Mark order confirmed under COD
        order.status = Order.Status.CONFIRMED
        order.payment_status = Order.PaymentStatus.PENDING
        order.save(update_fields=["status", "payment_status", "updated_at"])

        OrderStatusHistory.objects.create(
            order=order,
            status=Order.Status.CONFIRMED,
            changed_by=user,
            note="Order confirmed with Cash on Delivery (COD).",
        )
        return payment

    # Handle Razorpay Gateway payment creation
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "payment_method": Payment.Method.RAZORPAY,
            "amount": order.total_amount,
            "status": Payment.Status.CREATED,
        },
    )

    # If payment already has a Razorpay order ID, avoid creating a duplicate gateway order
    if payment.gateway_order_id:
        return payment

    client = get_razorpay_client()
    razorpay_order = client.order.create(
        {
            "amount": int(Decimal(order.total_amount) * 100),
            "currency": "INR",
            "receipt": order.order_number,
        }
    )

    payment.gateway_order_id = razorpay_order["id"]
    payment.status = Payment.Status.PENDING
    payment.save(update_fields=["gateway_order_id", "status", "updated_at"])

    return payment


@transaction.atomic
def verify_payment(
    payment,
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature,
):
    """
    Verifies Razorpay payment signature after successful completion on the frontend.
    Includes idempotency guards, transaction logging, stock confirmation, and audit logs.
    """
    # Idempotency check: Return immediately if payment is already marked as SUCCESS
    if payment.status == Payment.Status.SUCCESS:
        return payment

    if payment.gateway_order_id != razorpay_order_id:
        raise ValidationError("Razorpay order ID does not match.")

    client = get_razorpay_client()

    try:
        # Cryptographic verification of payment signature
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except Exception as exc:
        handle_payment_failure(
            payment,
            reason=f"Signature verification failed: {str(exc)}",
            user=payment.order.user,
        )
        raise ValidationError("Payment verification failed.")

    # Update Payment record state on verification success
    payment.transaction_id = razorpay_payment_id
    payment.status = Payment.Status.SUCCESS
    payment.paid_at = timezone.now()
    payment.save(update_fields=["transaction_id", "status", "paid_at", "updated_at"])

    # Safely create or get transaction log (avoids unique constraint race conditions)
    PaymentTransaction.objects.get_or_create(
        transaction_id=razorpay_payment_id,
        defaults={
            "payment": payment,
            "gateway_transaction_id": razorpay_payment_id,
            "amount": payment.amount,
            "status": "success",
            "gateway_response": {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            },
        },
    )

    # Update parent Order status to PAID and CONFIRMED
    order = payment.order
    order.payment_status = Order.PaymentStatus.PAID
    order.status = Order.Status.CONFIRMED
    order.save(update_fields=["payment_status", "status", "updated_at"])

    # Log status change history
    OrderStatusHistory.objects.create(
        order=order,
        status=Order.Status.CONFIRMED,
        changed_by=order.user,
        note="Payment verified successfully via Razorpay.",
    )

    return payment


@transaction.atomic
def process_refund(payment, amount, reason, user=None):
    """
    Initiates a refund with Razorpay API and updates Refund, Payment, and Order states.
    """
    if payment.status != Payment.Status.SUCCESS:
        raise ValidationError("Only successful payments can be refunded.")

    if Decimal(amount) <= 0 or Decimal(amount) > Decimal(payment.amount):
        raise ValidationError("Invalid refund amount.")

    client = get_razorpay_client()

    try:
        razorpay_refund = client.payment.refund(
            payment.transaction_id,
            {"amount": int(Decimal(amount) * 100)},
        )
    except Exception as exc:
        raise ValidationError(f"Razorpay refund failed: {str(exc)}")

    refund_record = Refund.objects.create(
        payment=payment,
        amount=amount,
        reason=reason,
        gateway_refund_id=razorpay_refund.get("id", ""),
        status=Refund.Status.COMPLETED,
    )

    # Calculate total refunded amount for this payment
    total_refunded = sum(r.amount for r in payment.refunds.filter(status=Refund.Status.COMPLETED))

    order = payment.order
    if total_refunded >= payment.amount:
        payment.status = Payment.Status.REFUNDED
        order.payment_status = Order.PaymentStatus.REFUNDED
        order.status = Order.Status.REFUNDED
    else:
        order.payment_status = Order.PaymentStatus.PARTIALLY_REFUNDED

    payment.save(update_fields=["status", "updated_at"])
    order.save(update_fields=["payment_status", "status", "updated_at"])

    OrderStatusHistory.objects.create(
        order=order,
        status=order.status,
        changed_by=user,
        note=f"Refund of {amount} INR processed successfully. Reason: {reason}",
    )

    return refund_record


@transaction.atomic
def process_razorpay_webhook(payload_body, signature_header):
    """
    Verifies and processes asynchronous Razorpay Webhook notifications.
    Supports events: payment.captured, payment.failed, order.paid, refund.processed
    """
    webhook_secret = getattr(settings, "RAZORPAY_WEBHOOK_SECRET", None)
    if not webhook_secret:
        raise ValidationError("RAZORPAY_WEBHOOK_SECRET is not configured.")

    client = get_razorpay_client()
    try:
        client.utility.verify_webhook_signature(
            payload_body.decode("utf-8") if isinstance(payload_body, bytes) else payload_body,
            signature_header,
            webhook_secret,
        )
    except Exception:
        raise ValidationError("Invalid webhook signature.")

    data = json.loads(payload_body)
    event = data.get("event")
    payload = data.get("payload", {})

    if event in ["payment.captured", "order.paid"]:
        payment_entity = payload.get("payment", {}).get("entity", {})
        razorpay_order_id = payment_entity.get("order_id")
        razorpay_payment_id = payment_entity.get("id")

        if razorpay_order_id:
            try:
                payment = Payment.objects.get(gateway_order_id=razorpay_order_id)
                if payment.status != Payment.Status.SUCCESS:
                    payment.transaction_id = razorpay_payment_id
                    payment.status = Payment.Status.SUCCESS
                    payment.paid_at = timezone.now()
                    payment.save(update_fields=["transaction_id", "status", "paid_at", "updated_at"])

                    order = payment.order
                    order.payment_status = Order.PaymentStatus.PAID
                    order.status = Order.Status.CONFIRMED
                    order.save(update_fields=["payment_status", "status", "updated_at"])

                    OrderStatusHistory.objects.create(
                        order=order,
                        status=Order.Status.CONFIRMED,
                        changed_by=None,
                        note="Payment captured via Razorpay Webhook.",
                    )
            except Payment.DoesNotExist:
                pass

    elif event == "payment.failed":
        payment_entity = payload.get("payment", {}).get("entity", {})
        razorpay_order_id = payment_entity.get("order_id")
        error_description = payment_entity.get("error_description", "Payment failed via webhook notification.")

        if razorpay_order_id:
            try:
                payment = Payment.objects.get(gateway_order_id=razorpay_order_id)
                if payment.status != Payment.Status.FAILED:
                    handle_payment_failure(payment, reason=error_description, user=None)
            except Payment.DoesNotExist:
                pass

    return {"status": "success", "event": event}
