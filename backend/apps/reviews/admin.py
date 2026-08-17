from django.contrib import admin

from .models import (
    Review,
    ReviewImage,
)


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "is_verified_purchase",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_verified_purchase",
        "is_approved",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__username",
        "user__email",
        "title",
        "comment",
    )

    readonly_fields = (
        "user",
        "order_item",
        "is_verified_purchase",
        "created_at",
        "updated_at",
    )

    inlines = [
        ReviewImageInline,
    ]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "review",
        "created_at",
    )

    search_fields = (
        "review__product__name",
        "review__user__username",
    )

    readonly_fields = (
        "created_at",
    )