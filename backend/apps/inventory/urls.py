from rest_framework.routers import DefaultRouter

from .views import (
    InventoryViewSet,
    InventoryTransactionViewSet,
)


router = DefaultRouter()

router.register(
    "inventory",
    InventoryViewSet,
    basename="inventory",
)

router.register(
    "transactions",
    InventoryTransactionViewSet,
    basename="inventory-transaction",
)

urlpatterns = router.urls