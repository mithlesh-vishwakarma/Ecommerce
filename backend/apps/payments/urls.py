from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    PaymentTransactionViewSet,
    RefundViewSet,
    CreatePaymentView,
    VerifyPaymentView,
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
]