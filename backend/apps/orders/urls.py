from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    OrderViewSet,
    CheckoutView,
)


router = DefaultRouter()

router.register(
    "orders",
    OrderViewSet,
    basename="order",
)


urlpatterns = router.urls + [
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout",
    ),
]