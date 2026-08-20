from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "brands",
    BrandViewSet,
    basename="brand",
)
router.register(
    "attributes",
    AttributeViewSet,
    basename="attribute",
)
router.register(
    "attribute-values",
    AttributeValueViewSet,
    basename="attribute-value",
)

router.register(
    "products",
    ProductViewSet,
    basename="product",
)
router.register(
    "product-images",
    ProductImageViewSet,
    basename="product-image",
)
router.register(
    "product-variants",
    ProductVariantViewSet,
    basename="product-variant",
)

urlpatterns = router.urls

# GET     /categories/
# POST    /categories/
# GET     /categories/{id}/
# PUT     /categories/{id}/
# PATCH   /categories/{id}/
# DELETE  /categories/{id}/


# GET     /brands/
# POST    /brands/
# GET     /brands/{id}/
# PUT     /brands/{id}/
# PATCH   /brands/{id}/
# DELETE  /brands/{id}/
