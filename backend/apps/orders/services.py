from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart
from apps.inventory.models import Inventory
from .models import Order, OrderItem, OrderStatusHistory


@transaction.atomic
def create_order_from_cart(
    user,
    shipping_address,
    billing_address=None,
    notes="",
):
    """
    Creates an Order from the user's active Cart in a single database transaction.
    
    Steps:
    1. Fetches and checks user's cart and cart items.
    2. Uses DB row-level locking (select_for_update) on Inventory records to avoid race conditions.
    3. Validates variant activity status and stock availability.
    4. Calculates prices and total amounts.
    5. Creates the Order record and OrderItems snapshots.
    6. Reserves the purchased quantity in Inventory.
    7. Creates initial OrderStatusHistory log.
    8. Clears the user's Cart after successful order creation.
    """
    try:
        cart = Cart.objects.prefetch_related(
            "items",
            "items__variant",
            "items__variant__product",
        ).get(user=user)
    except Cart.DoesNotExist:
        raise ValidationError("Cart does not exist.")

    cart_items = list(cart.items.all())

    if not cart_items:
        raise ValidationError("Your cart is empty.")

    # Lock inventory rows using select_for_update while checkout is processing
    variant_ids = [
        item.variant_id
        for item in cart_items
    ]

    inventories = {
        inventory.variant_id: inventory
        for inventory in Inventory.objects.select_for_update().filter(
            variant_id__in=variant_ids
        )
    }

    subtotal = Decimal("0.00")
    validated_items = []

    for cart_item in cart_items:
        variant = cart_item.variant
        product = variant.product

        if not variant.is_active:
            raise ValidationError(
                f"Variant {variant.sku} is no longer available."
            )

        inventory = inventories.get(
            variant.id
        )

        if inventory is None:
            raise ValidationError(
                f"No inventory found for {variant.sku}."
            )

        available_quantity = (
            inventory.quantity
            - inventory.reserved_quantity
        )

        if cart_item.quantity > available_quantity:
            raise ValidationError(
                f"Only {max(available_quantity, 0)} "
                f"units available for {variant.sku}."
            )

        # Variant price overrides product selling price if specified
        if variant.price is not None:
            unit_price = variant.price
        else:
            unit_price = product.selling_price

        total_price = (
            unit_price * cart_item.quantity
        )

        subtotal += total_price

        validated_items.append({
            "cart_item": cart_item,
            "variant": variant,
            "product": product,
            "inventory": inventory,
            "unit_price": unit_price,
            "total_price": total_price,
        })

    # Calculations for discount, shipping, tax
    discount_amount = Decimal("0.00")
    shipping_amount = Decimal("0.00")
    tax_amount = Decimal("0.00")

    total_amount = (
        subtotal
        - discount_amount
        + shipping_amount
        + tax_amount
    )

    # Create Order object in database
    order = Order.objects.create(
        user=user,
        order_number=generate_order_number(),
        status=Order.Status.PENDING,
        payment_status=Order.PaymentStatus.PENDING,
        subtotal=subtotal,
        discount_amount=discount_amount,
        shipping_amount=shipping_amount,
        tax_amount=tax_amount,
        total_amount=total_amount,
        shipping_address=shipping_address,
        billing_address=billing_address,
        notes=notes,
    )

    # Create OrderItem records & update reserved inventory quantity
    for item in validated_items:
        OrderItem.objects.create(
            order=order,
            variant=item["variant"],
            product_name=item["product"].name,
            sku=item["variant"].sku,
            quantity=item["cart_item"].quantity,
            unit_price=item["unit_price"],
            total_price=item["total_price"],
        )

        item["inventory"].reserved_quantity += (
            item["cart_item"].quantity
        )

        item["inventory"].save(
            update_fields=[
                "reserved_quantity",
                "updated_at",
            ]
        )

    # Log initial status in status history tracking
    OrderStatusHistory.objects.create(
        order=order,
        status=Order.Status.PENDING,
        changed_by=user,
        note="Order created from checkout.",
    )

    # Empty user's cart items after order is saved successfully
    cart.items.all().delete()

    return order


def generate_order_number():
    """
    Generates a unique order reference number using standard prefix and UUID prefix.
    Example: ORD-A1B2C3D4E5F6
    """
    import uuid

    return f"ORD-{uuid.uuid4().hex[:12].upper()}"