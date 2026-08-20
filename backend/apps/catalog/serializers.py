from rest_framework import serializers

from .models import (
    Category,
    Brand,
    Attribute,
    AttributeValue,
    Product,
    ProductImage,
    ProductVariant,
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
        ]



class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Attribute
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
            "values",
        ]

        read_only_fields = [
            "id",
            "slug",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "alt_text",
            "is_primary",
            "sort_order",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):

    attributes = AttributeValueSerializer(
        many=True,
        read_only=True,
    )

    attribute_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=AttributeValue.objects.filter(
            is_active=True
        ),
        source="attributes",
        required=False,
    )

    class Meta:
        model = ProductVariant

        fields = [
            "id",
            "product",
            "sku",
            "attributes",
            "attribute_ids",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True,
    )

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(
            is_active=True
        ),
        source="category",
        write_only=True,
    )

    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.filter(
            is_active=True
        ),
        source="brand",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "short_description",
            "description",
            "mrp",
            "selling_price",
            "is_active",
            "is_featured",
            "is_new_arrival",
            "is_best_seller",
            "images",
            "variants",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]


