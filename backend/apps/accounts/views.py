from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from django.contrib.auth.models import Group
from .permissions import IsSuperAdmin

User = get_user_model()


# ==========================================
# REGISTER VIEW
# ==========================================
class RegisterView(APIView):
    """
    API view for new user registration.
    Allows anyone to submit registration data, creates a new user, and returns access/refresh JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST request for user registration.
        """
        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate JWT refresh and access tokens for the newly registered user
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Registration successful.",
                "user": UserSerializer(user).data,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# LOGIN VIEW
# ==========================================
class LoginView(TokenObtainPairView):
    """
    API view for authenticating users via JWT.
    Uses custom LoginSerializer to attach user profile information to the response.
    """
    serializer_class = LoginSerializer


# ==========================================
# LOGOUT VIEW
# ==========================================
class LogoutView(APIView):
    """
    API view for logging out users.
    Blacklists the provided refresh token so it can no longer be used.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST request to blacklist the user's refresh token.
        """
        refresh_token = request.data.get(
            "refresh"
        )

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Logout successful."
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {
                    "detail": "Invalid refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# ==========================================
# CURRENT USER ME VIEW
# ==========================================
class MeView(APIView):
    """
    API view to get the current authenticated user's profile details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns serialized details of the requesting user.
        """
        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )


# ==========================================
# PROFILE VIEW (GET / PATCH)
# ==========================================
class ProfileView(APIView):
    """
    API view to view and partially update profile details for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns full profile information of current user.
        """
        return Response(
            UserSerializer(request.user).data
        )

    def patch(self, request):
        """
        Updates specific fields (like first_name, last_name, phone, profile_image).
        """
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            UserSerializer(request.user).data
        )


# ==========================================
# CHANGE PASSWORD VIEW
# ==========================================
class ChangePasswordView(APIView):
    """
    API view for changing the current user's password securely.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Validates old password and sets the new password.
        """
        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {
                    "old_password":
                    "Current password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(
            serializer.validated_data[
                "new_password"
            ]
        )

        user.save()

        return Response(
            {
                "message":
                "Password changed successfully."
            }
        )


# ==========================================
# ADDRESS LIST & CREATE VIEW
# ==========================================
class AddressListCreateView(ListCreateAPIView):
    """
    API view to list all addresses for the logged-in user, or create a new address.
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters addresses so users can only see their own addresses.
        """
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        """
        Automatically sets the user field to the currently logged-in user during creation.
        """
        serializer.save(
            user=self.request.user
        )


# ==========================================
# ADDRESS DETAIL VIEW (GET / PUT / DELETE)
# ==========================================
class AddressDetailView(
    RetrieveUpdateDestroyAPIView
):
    """
    API view to retrieve, update, or delete a specific address belonging to the logged-in user.
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters address queryset to ensure users can only access their own address.
        """
        return Address.objects.filter(
            user=self.request.user
        )


# ==========================================
# ADMIN ROLE LIST VIEW
# ==========================================
class RoleListView(ListAPIView):
    """
    API view for SuperAdmins to list all system roles (groups) and permissions.
    """
    queryset = Group.objects.prefetch_related(
        "permissions__content_type"
    ).all()

    serializer_class = RoleSerializer

    permission_classes = [
        IsSuperAdmin
    ]


# ==========================================
# ADMIN USER LIST & DETAIL VIEWS
# ==========================================
class AdminUserListView(ListAPIView):
    """
    API view for SuperAdmins to list all users in the system.
    """
    queryset = User.objects.prefetch_related(
        "groups"
    ).all()

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsSuperAdmin
    ]


class AdminUserDetailView(
    RetrieveUpdateAPIView
):
    """
    API view for SuperAdmins to retrieve and update user details or roles.
    """
    queryset = User.objects.prefetch_related(
        "groups"
    ).all()

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsSuperAdmin
    ]