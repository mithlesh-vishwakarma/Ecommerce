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


# ==========================================
# INVENTORY VIEWSET
# ==========================================
class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage inventory levels for product variants.
    Provides public read-only access and requires admin permissions for modifications.
    """
    queryset = Inventory.objects.select_related(
        "variant",
        "variant__product",
    ).all()

    serializer_class = InventorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [HasModelPermission()]


# ==========================================
# INVENTORY TRANSACTION VIEWSET
# ==========================================
class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet to record and view inventory transactions (stock audits, additions, deductions).
    Automatically attaches created_by user on creation.
    """
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
        """
        Automatically sets the creator to the requesting user.
        """
        serializer.save(created_by=self.request.user)