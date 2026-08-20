from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register(
    "cart",
    CartViewSet,
    basename="cart",
)

router.register(
    "items",
    CartItemViewSet,
    basename="cart-item",
)
router.register(
    "wishlist",
    WishlistViewSet,
    basename="wishlist",
)

router.register(
    "wishlist/items",
    WishlistItemViewSet,
    basename="wishlist-item",
)


urlpatterns = router.urls