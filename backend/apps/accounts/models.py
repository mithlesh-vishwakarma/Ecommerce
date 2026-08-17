from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    profile_image = models.ImageField(
        upload_to="users/profile/",
        blank=True,
        null=True,
    )

    is_customer = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email



class Address(models.Model):

    ADDRESS_TYPES = (
        ("home", "Home"),
        ("work", "Work"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default="home",
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    landmark = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    country = models.CharField(
        max_length=100,
        default="India",
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"