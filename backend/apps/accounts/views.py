from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateAPIView)
from django.contrib.auth.models import Group
from .permissions import IsSuperAdmin

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

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
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

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

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data
        )

    def patch(self, request):

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

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

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


class AddressListCreateView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

class AddressDetailView(
    RetrieveUpdateDestroyAPIView
):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )


class RoleListView(ListAPIView):

    queryset = Group.objects.prefetch_related(
        "permissions__content_type"
    ).all()

    serializer_class = RoleSerializer

    permission_classes = [
        IsSuperAdmin
    ]

class AdminUserListView(ListAPIView):

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

    queryset = User.objects.prefetch_related(
        "groups"
    ).all()

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsSuperAdmin
    ]