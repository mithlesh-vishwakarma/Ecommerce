from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import (
    Inventory,
    InventoryTransaction,
)

from .serializers import (
    InventorySerializer,
    InventoryTransactionSerializer,
)

from apps.accounts.permissions import HasModelPermission


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related(
        "variant",
        "variant__product",
    ).all()

    serializer_class = InventorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.select_related(
        "variant",
        "variant__product",
        "created_by",
    ).all()

    serializer_class = InventoryTransactionSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)