from rest_framework import serializers

from .models import Review, ReviewImage


class ReviewImageSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ReviewImage
        fields = [
            "id",
            "image",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Review

        fields = [
            "id",
            "product",
            "user",
            "order_item",
            "rating",
            "title",
            "comment",
            "is_verified_purchase",
            "is_approved",
            "images",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "order_item",
            "is_verified_purchase",
            "is_approved",
            "images",
            "created_at",
            "updated_at",
        ]