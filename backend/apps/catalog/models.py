from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ----------------------------------------------------------------

class Brand(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




# ----------------------------------------------------------------

class Attribute(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# --------------------------values--------------------------


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=120,
        blank=True,
    )

    color_code = models.CharField(
        max_length=20,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["attribute", "value"],
                name="unique_attribute_value",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.value)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# ----------------------------------------------------------------


class Product(models.Model):
    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
    )

    description = models.TextField(blank=True)

    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(default=True)

    is_featured = models.BooleanField(default=False)

    is_new_arrival = models.BooleanField(default=False)

    is_best_seller = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





# ----------------------------------------------------------------


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/",
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(default=False)

    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} image"



# -------------------------------------------------------------------


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    attributes = models.ManyToManyField(
        AttributeValue,
        related_name="variants",
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.product.name} - {self.sku}"