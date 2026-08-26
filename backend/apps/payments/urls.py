from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    PaymentTransactionViewSet,
    RefundViewSet,
    CreatePaymentView,
    VerifyPaymentView,
    CancelPaymentView,
    InitiateRefundView,
    RazorpayWebhookView,
)


router = DefaultRouter()

router.register(
    "payments",
    PaymentViewSet,
    basename="payment",
)

router.register(
    "transactions",
    PaymentTransactionViewSet,
    basename="payment-transaction",
)

router.register(
    "refunds",
    RefundViewSet,
    basename="refund",
)


urlpatterns = router.urls + [
    path(
        "create/",
        CreatePaymentView.as_view(),
        name="create-payment",
    ),
    path(
        "verify/",
        VerifyPaymentView.as_view(),
        name="verify-payment",
    ),
    path(
        "cancel/",
        CancelPaymentView.as_view(),
        name="cancel-payment",
    ),
    path(
        "refund/initiate/",
        InitiateRefundView.as_view(),
        name="initiate-refund",
    ),
    path(
        "webhook/",
        RazorpayWebhookView.as_view(),
        name="razorpay-webhook",
    ),
]