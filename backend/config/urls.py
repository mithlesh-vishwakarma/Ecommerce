from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # JWT Tokens
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # Authentication
    path(
        "api/auth/",
        include("apps.accounts.urls")
    ),
    #catalog
    path(
        "api/catalog/",
        include("apps.catalog.urls")
    ),
    path(
        "api/inventory/",
        include("apps.inventory.urls"),
    ),
    path(
        "api/cart/",
        include("apps.cart.urls"),
    ),
    path(
    "api/orders/",
    include("apps.orders.urls"),
    ),
    path(
    "api/payments/",
    include("apps.payments.urls"),
),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
