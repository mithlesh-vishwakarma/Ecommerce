from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order
from django.conf import settings
from .services import *


# ==========================================
# PAYMENT VIEWSET
# ==========================================
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for customers to view payment history attached to their orders.
    """
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """
        Ensures users only access payment records for their own orders.
        """
        return Payment.objects.filter(
            order__user=self.request.user
        ).select_related(
            "order",
            "order__user",
        ).prefetch_related(
            "transactions",
            "refunds",
        )

    def get_permissions(self):
        return [IsAuthenticated()]


# ==========================================
# PAYMENT TRANSACTION VIEWSET
# ==========================================
class PaymentTransactionViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """
    Read-only viewset for gateway transactions belonging to the user's orders.
    """
    serializer_class = PaymentTransactionSerializer

    def get_queryset(self):
        return PaymentTransaction.objects.filter(
            payment__order__user=self.request.user
        ).select_related(
            "payment",
            "payment__order",
        )

    def get_permissions(self):
        return [IsAuthenticated()]


# ==========================================
# REFUND VIEWSET
# ==========================================
class RefundViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for tracking user refund records.
    """
    serializer_class = RefundSerializer

    def get_queryset(self):
        return Refund.objects.filter(
            payment__order__user=self.request.user
        ).select_related(
            "payment",
            "payment__order",
        )

    def get_permissions(self):
        return [IsAuthenticated()]


# ==========================================
# CREATE PAYMENT VIEW (RAZORPAY)
# ==========================================
class CreatePaymentView(APIView):
    """
    API view to initiate Razorpay payment for an order.
    Creates or retrieves local Payment record and requests a Razorpay order ID.
    """
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):
        """
        Handles payment initiation.
        Returns Razorpay order ID and public Razorpay Key ID for checkout popup in frontend.
        """
        order_id = request.data.get(
            "order_id"
        )

        if not order_id:
            raise ValidationError(
                {
                    "order_id":
                    "Order ID is required."
                }
            )

        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user,
            )

        except Order.DoesNotExist:
            raise ValidationError(
                {
                    "order_id":
                    "Order not found."
                }
            )

        payment = create_payment_order(
            order=order,
            user=request.user,
        )

        return Response(
            {
                "message":
                    "Payment order created.",

                "payment": {
                    "id": payment.id,
                    "order_id": order.id,
                    "amount": payment.amount,
                    "currency": "INR",
                    "payment_method":
                        payment.payment_method,
                    "gateway_order_id":
                        payment.gateway_order_id,
                    "razorpay_key_id":
                        settings.RAZORPAY_KEY_ID,
                    "status": payment.status,
                }
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# VERIFY PAYMENT VIEW (RAZORPAY SIGNATURE)
# ==========================================
class VerifyPaymentView(APIView):
    """
    API view to verify cryptographic HMAC signature sent back by Razorpay frontend SDK.
    On successful signature verification, marks payment as SUCCESS and order as PAID.
    """
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):
        """
        Verifies razorpay_order_id, razorpay_payment_id, and razorpay_signature.
        """
        payment_id = request.data.get(
            "payment_id"
        )

        razorpay_order_id = request.data.get(
            "razorpay_order_id"
        )

        razorpay_payment_id = request.data.get(
            "razorpay_payment_id"
        )

        razorpay_signature = request.data.get(
            "razorpay_signature"
        )

        if not all([
            payment_id,
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature,
        ]):
            raise ValidationError(
                "All payment verification fields are required."
            )

        try:
            payment = Payment.objects.select_related(
                "order"
            ).get(
                id=payment_id,
                order__user=request.user,
            )

        except Payment.DoesNotExist:
            raise ValidationError(
                "Payment not found."
            )

        payment = verify_payment(
            payment=payment,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )

        return Response(
            {
                "message":
                    "Payment verified successfully.",

                "payment":
                    PaymentSerializer(payment).data,
            },
            status=status.HTTP_200_OK,
        )