from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer

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