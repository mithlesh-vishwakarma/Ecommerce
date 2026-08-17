from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create default ecommerce roles and assign permissions."

    ROLE_PERMISSIONS = {
        "Product Manager": [
            "catalog.view_product",
            "catalog.add_product",
            "catalog.change_product",
            "catalog.view_productimage",
            "catalog.add_productimage",
            "catalog.change_productimage",
            "catalog.view_productvariant",
            "catalog.add_productvariant",
            "catalog.change_productvariant",
            "catalog.view_category",
            "catalog.add_category",
            "catalog.change_category",
            "catalog.view_brand",
            "catalog.add_brand",
            "catalog.change_brand",
            "catalog.view_attribute",
            "catalog.add_attribute",
            "catalog.change_attribute",
            "catalog.view_attributevalue",
            "catalog.add_attributevalue",
            "catalog.change_attributevalue",
        ],

        "Order Manager": [
            "orders.view_order",
            "orders.change_order",
            "orders.view_orderitem",
            "orders.view_orderstatushistory",
        ],

        "Inventory Manager": [
            "inventory.view_inventory",
            "inventory.change_inventory",
            "inventory.view_inventorytransaction",
            "inventory.add_inventorytransaction",
        ],

        "Marketing Manager": [
            "marketing.view_coupon",
            "marketing.add_coupon",
            "marketing.change_coupon",
            "marketing.view_couponusage",
        ],

        "Customer Support": [
            "accounts.view_user",
            "accounts.view_address",
            "orders.view_order",
            "orders.change_order",
            "orders.view_orderitem",
            "reviews.view_review",
            "reviews.change_review",
        ],
    }

    def handle(self, *args, **options):

        for role_name, permission_codes in self.ROLE_PERMISSIONS.items():

            group, created = Group.objects.get_or_create(
                name=role_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created role: {role_name}"
                    )
                )
            else:
                self.stdout.write(
                    f"Role already exists: {role_name}"
                )

            permissions = []

            for permission_code in permission_codes:

                try:
                    app_label, codename = permission_code.split(
                        "."
                    )

                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename,
                    )

                    permissions.append(permission)

                except Permission.DoesNotExist:

                    self.stdout.write(
                        self.style.WARNING(
                            f"Permission not found: "
                            f"{permission_code}"
                        )
                    )

            group.permissions.set(permissions)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated permissions for: {role_name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles created successfully."
            )
        )