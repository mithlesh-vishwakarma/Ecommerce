from django.contrib import admin

from .models import (
    Cart,
    CartItem,
    Wishlist,
    WishlistItem,
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "item_count",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        CartItemInline,
    ]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "variant",
        "quantity",
        "created_at",
    )

    search_fields = (
        "cart__user__username",
        "cart__user__email",
        "variant__sku",
    )


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    inlines = [
        WishlistItemInline,
    ]


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "wishlist",
        "product",
        "created_at",
    )

    search_fields = (
        "wishlist__user__username",
        "wishlist__user__email",
        "product__name",
    )