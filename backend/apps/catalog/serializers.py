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


# ==========================================
# CATEGORY SERIALIZER
# ==========================================
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Product Categories (e.g. Electronics, Clothing).
    Converts Category instances into JSON and handles auto-generated slug/timestamps.
    """
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]


# ==========================================
# BRAND SERIALIZER
# ==========================================
class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Brands (e.g. Nike, Apple, Samsung).
    """
    class Meta:
        model = Brand
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]


# ==========================================
# ATTRIBUTE VALUE SERIALIZER
# ==========================================
class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer for specific values of an attribute (e.g., "Red", "Blue", "XL", "64GB").
    """
    class Meta:
        model = AttributeValue
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
        ]


# ==========================================
# ATTRIBUTE SERIALIZER
# ==========================================
class AttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Attributes (e.g., "Color", "Size").
    Includes nested serializations of all associated attribute values.
    """
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


# ==========================================
# PRODUCT IMAGE SERIALIZER
# ==========================================
class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for gallery images attached to a product.
    Includes primary image status and sorting order.
    """
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


# ==========================================
# PRODUCT VARIANT SERIALIZER
# ==========================================
class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for specific product variations (SKU, price override, attributes like Size+Color).
    Supports reading attribute details and writing attribute IDs.
    """
    attributes = AttributeValueSerializer(
        many=True,
        read_only=True,
    )

    # Accepts attribute value IDs during creation/update
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


# ==========================================
# PRODUCT SERIALIZER
# ==========================================
class ProductSerializer(serializers.ModelSerializer):
    """
    Comprehensive Serializer for Product details.
    Combines nested details for Category, Brand, Images, and Variants for full frontend rendering.
    """
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

    # Primary key inputs for foreign key assignment on create/update
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



