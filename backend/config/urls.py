from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # JWT Tokens
    path(
        "api/v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/v1/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # Authentication
    path(
        "api/v1/auth/",
        include("apps.accounts.urls")
    ),
    #catalog
    path(
        "api/v1/catalog/",
        include("apps.catalog.urls")
    ),
    path(
        "api/v1/inventory/",
        include("apps.inventory.urls"),
    ),
    path(
        "api/v1/cart/",
        include("apps.cart.urls"),
    ),
    path(
    "api/v1/orders/",
    include("apps.orders.urls"),
    ),
    path(
    "api/v1/payments/",
    include("apps.payments.urls"),
),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
