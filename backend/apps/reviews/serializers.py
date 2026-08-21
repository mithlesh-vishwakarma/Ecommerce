from rest_framework import serializers

from .models import Review, ReviewImage


# ==========================================
# REVIEW IMAGE SERIALIZER
# ==========================================
class ReviewImageSerializer(
    serializers.ModelSerializer
):
    """
    Serializer for photos uploaded by users attached to product reviews.
    """
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


# ==========================================
# REVIEW SERIALIZER
# ==========================================
class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for customer product reviews and ratings (1 to 5 stars).
    Includes verified purchase tags and admin approval status.
    """
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