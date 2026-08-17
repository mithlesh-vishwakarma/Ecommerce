from django.db import models


class Payment(models.Model):

    class Method(models.TextChoices):
        RAZORPAY = "razorpay", "Razorpay"
        COD = "cod", "Cash on Delivery"

    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payment",
    )

    payment_method = models.CharField(
        max_length=30,
        choices=Method.choices,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    gateway_order_id = models.CharField(
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"


class PaymentTransaction(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
    )

    gateway_transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=30,
    )

    gateway_response = models.JSONField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.transaction_id


class Refund(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name="refunds",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reason = models.TextField()

    gateway_refund_id = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.payment.order.order_number} - {self.amount}"


