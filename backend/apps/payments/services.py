from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

import razorpay

from django.conf import settings

from .models import Payment, PaymentTransaction
from apps.orders.models import Order


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
def create_payment_order(order, user):
    """
    Creates a payment session with Razorpay for the given Order.
    Converts total amount into paise (amount * 100) as required by Razorpay API.
    """
    if order.user_id != user.id:
        raise ValidationError(
            "You are not allowed to pay for this order."
        )

    if order.payment_status == Order.PaymentStatus.PAID:
        raise ValidationError(
            "This order has already been paid."
        )

    # Get or create our local Payment record
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "payment_method": Payment.Method.RAZORPAY,
            "amount": order.total_amount,
            "status": Payment.Status.CREATED,
        },
    )

    # If payment already has a Razorpay order ID, avoid creating a duplicate order
    if payment.gateway_order_id:
        return payment

    client = get_razorpay_client()

    # Razorpay expects amounts in minimum currency units (e.g. 1 INR = 100 paise)
    razorpay_order = client.order.create(
        {
            "amount": int(
                Decimal(order.total_amount) * 100
            ),
            "currency": "INR",
            "receipt": order.order_number,
        }
    )

    payment.gateway_order_id = razorpay_order["id"]
    payment.status = Payment.Status.PENDING

    payment.save(
        update_fields=[
            "gateway_order_id",
            "status",
            "updated_at",
        ]
    )

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
    Updates payment status, creates transaction log, and updates Order status to PAID/CONFIRMED.
    """
    if payment.gateway_order_id != razorpay_order_id:
        raise ValidationError(
            "Razorpay order ID does not match."
        )

    client = get_razorpay_client()

    try:
        # Cryptographic verification of payment signature
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id":
                    razorpay_order_id,

                "razorpay_payment_id":
                    razorpay_payment_id,

                "razorpay_signature":
                    razorpay_signature,
            }
        )

    except Exception:
        payment.status = Payment.Status.FAILED

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        raise ValidationError(
            "Payment verification failed."
        )

    # Update Payment record state on verification success
    payment.transaction_id = razorpay_payment_id
    payment.status = Payment.Status.SUCCESS
    payment.paid_at = timezone.now()

    payment.save(
        update_fields=[
            "transaction_id",
            "status",
            "paid_at",
            "updated_at",
        ]
    )

    # Save transaction details in local database
    transaction_record = PaymentTransaction.objects.create(
        payment=payment,
        transaction_id=razorpay_payment_id,
        gateway_transaction_id=razorpay_payment_id,
        amount=payment.amount,
        status="success",
        gateway_response={
            "razorpay_order_id":
                razorpay_order_id,
            "razorpay_payment_id":
                razorpay_payment_id,
            "razorpay_signature":
                razorpay_signature,
        },
    )

    # Update parent Order status to PAID and CONFIRMED
    order = payment.order

    order.payment_status = (
        Order.PaymentStatus.PAID
    )

    order.status = Order.Status.CONFIRMED

    order.save(
        update_fields=[
            "payment_status",
            "status",
            "updated_at",
        ]
    )

    return payment