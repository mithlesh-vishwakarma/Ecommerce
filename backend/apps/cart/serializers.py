from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
)


class CartItemSerializer(serializers.ModelSerializer):
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


class CartSerializer(serializers.ModelSerializer):
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


class WishlistItemSerializer(serializers.ModelSerializer):
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


class WishlistSerializer(serializers.ModelSerializer):
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