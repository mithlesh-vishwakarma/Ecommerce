from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.conf import settings
from apps.orders.models import Order
from .models import Payment, PaymentTransaction, Refund
from .serializers import PaymentSerializer, PaymentTransactionSerializer, RefundSerializer
from .services import (
    create_payment_order,
    verify_payment,
    process_refund,
    handle_payment_failure,
    process_razorpay_webhook,
)


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
class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
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
# CREATE PAYMENT VIEW (RAZORPAY / COD)
# ==========================================
class CreatePaymentView(APIView):
    """
    API view to initiate payment (Razorpay or COD) for an order.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method", Payment.Method.RAZORPAY)

        if not order_id:
            raise ValidationError({"order_id": "Order ID is required."})

        if payment_method not in [Payment.Method.RAZORPAY, Payment.Method.COD]:
            raise ValidationError({"payment_method": "Invalid payment method."})

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            raise ValidationError({"order_id": "Order not found."})

        payment = create_payment_order(
            order=order,
            user=request.user,
            payment_method=payment_method,
        )

        return Response(
            {
                "message": "Payment order initialized.",
                "payment": {
                    "id": payment.id,
                    "order_id": order.id,
                    "amount": payment.amount,
                    "currency": "INR",
                    "payment_method": payment.payment_method,
                    "gateway_order_id": payment.gateway_order_id,
                    "razorpay_key_id": getattr(settings, "RAZORPAY_KEY_ID", ""),
                    "status": payment.status,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# VERIFY PAYMENT VIEW (RAZORPAY SIGNATURE)
# ==========================================
class VerifyPaymentView(APIView):
    """
    API view to verify cryptographic HMAC signature sent back by Razorpay frontend SDK.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not all([payment_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            raise ValidationError("All payment verification fields are required.")

        try:
            payment = Payment.objects.select_related("order").get(
                id=payment_id,
                order__user=request.user,
            )
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        payment = verify_payment(
            payment=payment,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )

        return Response(
            {
                "message": "Payment verified successfully.",
                "payment": PaymentSerializer(payment).data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# CANCEL PAYMENT VIEW (RELEASE STOCK)
# ==========================================
class CancelPaymentView(APIView):
    """
    API view to cancel payment and release reserved stock if user aborts checkout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")
        reason = request.data.get("reason", "Cancelled by user.")

        if not payment_id:
            raise ValidationError({"payment_id": "Payment ID is required."})

        try:
            payment = Payment.objects.select_related("order").get(
                id=payment_id,
                order__user=request.user,
            )
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        payment = handle_payment_failure(payment, reason=reason, user=request.user)

        return Response(
            {
                "message": "Payment cancelled and reserved inventory released.",
                "payment": PaymentSerializer(payment).data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# INITIATE REFUND VIEW (ADMIN ONLY)
# ==========================================
class InitiateRefundView(APIView):
    """
    API view for admins/staff to process payment refunds.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        payment_id = request.data.get("payment_id")
        amount = request.data.get("amount")
        reason = request.data.get("reason", "Admin initiated refund.")

        if not payment_id or amount is None:
            raise ValidationError({"error": "payment_id and amount are required."})

        try:
            payment = Payment.objects.select_related("order").get(id=payment_id)
        except Payment.DoesNotExist:
            raise ValidationError({"payment_id": "Payment not found."})

        refund_record = process_refund(
            payment=payment,
            amount=amount,
            reason=reason,
            user=request.user,
        )

        return Response(
            {
                "message": "Refund processed successfully.",
                "refund": RefundSerializer(refund_record).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# RAZORPAY WEBHOOK VIEW
# ==========================================
class RazorpayWebhookView(APIView):
    """
    Public webhook endpoint to receive asynchronous events from Razorpay server.
    Verifies signature with RAZORPAY_WEBHOOK_SECRET.
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        signature_header = request.headers.get("X-Razorpay-Signature")
        if not signature_header:
            raise ValidationError("X-Razorpay-Signature header is missing.")

        result = process_razorpay_webhook(
            payload_body=request.body,
            signature_header=signature_header,
        )

        return Response(result, status=status.HTTP_200_OK)
