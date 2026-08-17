from django.contrib import admin

from .models import (
    Category,
    Brand,
    Attribute,
    AttributeValue,
    Product,
    ProductImage,
    ProductVariant,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "parent",
        "is_active",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "parent",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "sort_order",
        "name",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        AttributeValueInline,
    ]


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "attribute",
        "value",
        "color_code",
        "is_active",
    )

    list_filter = (
        "attribute",
        "is_active",
    )

    search_fields = (
        "value",
        "attribute__name",
    )

    prepopulated_fields = {
        "slug": ("value",)
    }


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    filter_horizontal = (
        "attributes",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "sku",
        "category",
        "brand",
        "mrp",
        "selling_price",
        "is_active",
        "is_featured",
        "is_new_arrival",
        "is_best_seller",
        "created_at",
    )

    list_filter = (
        "is_active",
        "is_featured",
        "is_new_arrival",
        "is_best_seller",
        "category",
        "brand",
    )

    search_fields = (
        "name",
        "sku",
        "description",
        "category__name",
        "brand__name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        ProductImageInline,
        ProductVariantInline,
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "is_primary",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "alt_text",
    )

    ordering = (
        "product",
        "sort_order",
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "sku",
        "price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "product",
    )

    search_fields = (
        "sku",
        "product__name",
        "product__sku",
    )

    filter_horizontal = (
        "attributes",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )