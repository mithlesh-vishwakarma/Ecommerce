from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    ProfileView,
    ChangePasswordView,
    AddressListCreateView,
    AddressDetailView,
    RoleListView,
    AdminUserListView,
    AdminUserDetailView,
)


urlpatterns = [

    # =========================
    # AUTHENTICATION
    # =========================

    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),


    # =========================
    # ADDRESSES
    # =========================

    path(
        "addresses/",
        AddressListCreateView.as_view(),
        name="address-list-create",
    ),

    path(
        "addresses/<int:pk>/",
        AddressDetailView.as_view(),
        name="address-detail",
    ),


    # =========================
    # ADMIN - ROLES & USERS
    # =========================

    path(
        "admin/roles/",
        RoleListView.as_view(),
        name="admin-roles",
    ),

    path(
        "admin/users/",
        AdminUserListView.as_view(),
        name="admin-users",
    ),

    path(
        "admin/users/<int:pk>/",
        AdminUserDetailView.as_view(),
        name="admin-user-detail",
    ),
]