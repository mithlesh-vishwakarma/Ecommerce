from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

from apps.accounts.permissions import HasModelPermission


# ==========================================
# CATEGORY VIEWSET
# ==========================================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, updating, and deleting product categories.
    Allows public read access while restricting write permissions to staff/admins.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Anyone can view categories (list and retrieve actions)
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Creating, updating, or deleting requires appropriate Django permissions
        return [HasModelPermission()]


# ==========================================
# BRAND VIEWSET
# ==========================================
class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product brands (e.g. Nike, Apple).
    Allows public access for viewing and permission-restricted access for modifications.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        # Public access for viewing brands
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create/update/delete require appropriate Django model permissions
        return [HasModelPermission()]


# ==========================================
# ATTRIBUTE VIEWSET
# ==========================================
class AttributeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product attributes (e.g. Color, Size, Storage Capacity).
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get_permissions(self):
        # Anyone can view attributes
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create / update / delete requires appropriate Django model permissions
        return [HasModelPermission()]


# ==========================================
# ATTRIBUTE VALUE VIEWSET
# ==========================================
class AttributeValueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing specific attribute values (e.g. Red, Blue, XL).
    Optimizes queries by selecting related attribute.
    """
    queryset = AttributeValue.objects.select_related("attribute").all()
    serializer_class = AttributeValueSerializer

    def get_permissions(self):
        # Anyone can view attribute values
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create / update / delete requires appropriate Django model permissions
        return [HasModelPermission()]


# ==========================================
# PRODUCT VIEWSET
# ==========================================
class ProductViewSet(viewsets.ModelViewSet):
    """
    Main ViewSet for product catalog listing and management.
    Uses select_related and prefetch_related to optimize DB queries for category, brand, images, and variants.
    """
    queryset = Product.objects.select_related(
        "category",
        "brand",
    ).prefetch_related(
        "images",
        "variants",
    ).all()

    serializer_class = ProductSerializer

    def get_permissions(self):
        # Public access for viewing products
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]


# ==========================================
# PRODUCT IMAGE VIEWSET
# ==========================================
class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product gallery images.
    """
    queryset = ProductImage.objects.select_related("product").all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]


# ==========================================
# PRODUCT VARIANT VIEWSET
# ==========================================
class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product variants (SKUs, specific pricing, and options).
    """
    queryset = ProductVariant.objects.prefetch_related(
        "attributes"
    ).select_related(
        "product"
    ).all()

    serializer_class = ProductVariantSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]