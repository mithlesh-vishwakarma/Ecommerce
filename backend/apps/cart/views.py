from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import *
from .serializers import *

from apps.accounts.permissions import HasModelPermission


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__variant",
            "items__variant__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
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
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        variant = serializer.validated_data["variant"]

        if not variant.is_active:
            raise PermissionDenied(
                "This product variant is not available."
            )

        serializer.save(cart=cart)

class WishlistViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__product",
            "items__product__product",
        )

    def get_permissions(self):
        return [HasModelPermission()]


class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
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
        wishlist, created = Wishlist.objects.get_or_create(
            user=self.request.user
        )

        product_variant = serializer.validated_data["product"]

        if not product_variant.is_active:
            raise PermissionDenied(
                "This product variant is not available."
            )

        serializer.save(wishlist=wishlist)