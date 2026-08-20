from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from apps.accounts.models import Address
from .services import create_order_from_cart
from .models import Order
from .serializers import OrderSerializer,CheckoutSerializer

from apps.accounts.permissions import HasModelPermission


class OrderViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        # Staff/admin can see all orders if they have permission
        if user.is_staff:
            return Order.objects.select_related(
                "user"
            ).prefetch_related(
                "items",
                "items__variant",
                "status_history",
                "status_history__changed_by",
            ).all()

        # Customers can only see their own orders
        return Order.objects.filter(
            user=user
        ).select_related(
            "user"
        ).prefetch_related(
            "items",
            "items__variant",
            "status_history",
            "status_history__changed_by",
        )

    def get_permissions(self):
        return [IsAuthenticated()]


class CheckoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = CheckoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        shipping_address_id = (
            serializer.validated_data[
                "shipping_address_id"
            ]
        )

        billing_address_id = (
            serializer.validated_data.get(
                "billing_address_id"
            )
        )

        notes = serializer.validated_data.get(
            "notes",
            "",
        )

        # Make sure shipping address belongs
        # to the logged-in user
        try:
            shipping_address = Address.objects.get(
                id=shipping_address_id,
                user=request.user,
            )
        except Address.DoesNotExist:
            raise ValidationError(
                {
                    "shipping_address_id":
                    "Shipping address not found."
                }
            )

        billing_address = None

        if billing_address_id:

            try:
                billing_address = Address.objects.get(
                    id=billing_address_id,
                    user=request.user,
                )

            except Address.DoesNotExist:
                raise ValidationError(
                    {
                        "billing_address_id":
                        "Billing address not found."
                    }
                )

        # Convert addresses into snapshots
        shipping_address_data = {
            "address_type": shipping_address.address_type,
            "full_name": shipping_address.full_name,
            "phone": shipping_address.phone,
            "address_line_1": shipping_address.address_line_1,
            "address_line_2": shipping_address.address_line_2,
            "landmark": shipping_address.landmark,
            "city": shipping_address.city,
            "state": shipping_address.state,
            "postal_code": shipping_address.postal_code,
            "country": shipping_address.country,
        }

        billing_address_data = None

        if billing_address:

            billing_address_data = {
                "address_type": billing_address.address_type,
                "full_name": billing_address.full_name,
                "phone": billing_address.phone,
                "address_line_1": billing_address.address_line_1,
                "address_line_2": billing_address.address_line_2,
                "landmark": billing_address.landmark,
                "city": billing_address.city,
                "state": billing_address.state,
                "postal_code": billing_address.postal_code,
                "country": billing_address.country,
            }

        order = create_order_from_cart(
            user=request.user,
            shipping_address=shipping_address_data,
            billing_address=billing_address_data,
            notes=notes,
        )

        return Response(
            {
                "message": "Order created successfully.",
                "order": OrderSerializer(
                    order
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )