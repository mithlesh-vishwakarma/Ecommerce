from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import *
from .serializers import *

from apps.accounts.permissions import HasModelPermission


# ==========================================
# CART VIEWSET
# ==========================================
class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for displaying the authenticated user's shopping cart and cart items.
    """
    serializer_class = CartSerializer

    def get_queryset(self):
        """
        Retrieves the cart for the logged-in user and optimizes DB queries using prefetch_related.
        """
        return Cart.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__variant",
            "items__variant__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]


# ==========================================
# CART ITEM VIEWSET
# ==========================================
class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for adding, updating, and removing items in the shopping cart.
    """
    serializer_class = CartItemSerializer

    def get_queryset(self):
        """
        Filters cart items to ensure users can only manage items in their own cart.
        """
        return CartItem.objects.filter(
            cart__user=self.request.user
        ).select_related(
            "cart",
            "variant",
            "variant__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]

    def perform_create(self, serializer):
        """
        Checks product availability and links the created CartItem to the user's Cart.
        """
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        variant = serializer.validated_data["variant"]

        if not variant.is_active:
            raise PermissionDenied(
                "This product variant is not available."
            )

        serializer.save(cart=cart)


# ==========================================
# WISHLIST VIEWSET
# ==========================================
class WishlistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for retrieving the user's wishlist and wishlist items.
    """
    serializer_class = WishlistSerializer

    def get_queryset(self):
        """
        Filters wishlist by logged-in user and prefetches related product data.
        """
        return Wishlist.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__product",
            "items__product__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]


# ==========================================
# WISHLIST ITEM VIEWSET
# ==========================================
class WishlistItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for adding, listing, and removing items from a wishlist.
    """
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        """
        Filters wishlist items to only those owned by the authenticated user.
        """
        return WishlistItem.objects.filter(
            wishlist__user=self.request.user
        ).select_related(
            "wishlist",
            "product",
            "product__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]

    def perform_create(self, serializer):
        """
        Verifies product variant status and associates the item with the user's Wishlist.
        """
        wishlist, created = Wishlist.objects.get_or_create(
            user=self.request.user
        )

        product_variant = serializer.validated_data["product"]

        if not product_variant.is_active:
            raise PermissionDenied(
                "This product variant is not available."
            )

        serializer.save(wishlist=wishlist)