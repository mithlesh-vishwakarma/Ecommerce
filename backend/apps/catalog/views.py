from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

from apps.accounts.permissions import HasModelPermission


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    def get_permissions(self):

        # Anyone can view categories
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Creating/updating/deleting requires
        # the appropriate Django permission
        return [HasModelPermission()]



class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()

    serializer_class = BrandSerializer

    def get_permissions(self):

        # Public access for viewing brands
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create/update/delete require
        # appropriate Django model permissions
        return [HasModelPermission()]


class AttributeViewSet(viewsets.ModelViewSet):

    queryset = Attribute.objects.all()

    serializer_class = AttributeSerializer

    def get_permissions(self):

        # Anyone can view attributes
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create / update / delete requires
        # the appropriate Django model permission
        return [HasModelPermission()]
    
class AttributeValueViewSet(viewsets.ModelViewSet):

    queryset = AttributeValue.objects.select_related("attribute").all()

    serializer_class = AttributeValueSerializer

    def get_permissions(self):

        # Anyone can view attribute values
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Create / update / delete requires
        # appropriate Django model permissions
        return [HasModelPermission()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "category",
        "brand",
    ).prefetch_related(
        "images",
        "variants",
    ).all()

    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related("product").all()

    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]


class ProductVariantViewSet(viewsets.ModelViewSet):
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