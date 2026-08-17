from django.db import models


class Coupon(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    minimum_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    starts_at = models.DateTimeField()

    expires_at = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code


class CouponUsage(models.Model):
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name="usages",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="coupon_usages",
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="coupon_usages",
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    used_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["coupon", "user", "order"],
                name="unique_coupon_user_order",
            )
        ]

    def __str__(self):
        return f"{self.coupon.code} - {self.user.email}"


