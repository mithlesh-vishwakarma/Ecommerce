from django.contrib import admin
from django.urls import path,include
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
    
]