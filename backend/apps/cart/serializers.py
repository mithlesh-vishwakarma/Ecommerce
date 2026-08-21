from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
)


# ==========================================
# CART ITEM SERIALIZER
# ==========================================
class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual items inside a shopping cart.
    Maps a product variant and its selected quantity.
    """
    class Meta:
        model = CartItem
        fields = [
            "id",
            "variant",
            "quantity",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ==========================================
# CART SERIALIZER
# ==========================================
class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the main shopping cart object.
    Includes nested serialization for cart items.
    """
    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# ==========================================
# WISHLIST ITEM SERIALIZER
# ==========================================
class WishlistItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual items added to a user's wishlist.
    """
    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


# ==========================================
# WISHLIST SERIALIZER
# ==========================================
class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for a user's full wishlist, containing nested wishlist items.
    """
    items = WishlistItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]