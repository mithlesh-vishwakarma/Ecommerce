from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = (
        "address_type",
        "full_name",
        "phone",
        "city",
        "state",
        "postal_code",
        "is_default",
    )


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "is_customer",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (
            "Login Information",
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "profile_image",
                )
            },
        ),
        (
            "Permissions & Roles",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_customer",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    inlines = [
        AddressInline,
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "user",
        "phone",
        "city",
        "state",
        "postal_code",
        "address_type",
        "is_default",
    )

    list_filter = (
        "address_type",
        "state",
        "is_default",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "postal_code",
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )