from rest_framework import serializers
from .models import User, Address
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_image",
            "is_customer",
            "is_staff",
            "is_active",
            "date_joined",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_customer",
            "is_staff",
            "is_active",
            "date_joined",
            "created_at",
        ]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_type",
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "landmark",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password2 = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "phone",
            "profile_image",
        ]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True,
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    new_password2 = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({
                "new_password": "Passwords do not match."
            })

        return attrs

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = [
            "id",
            "address_type",
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "landmark",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = user.id
        token["email"] = user.email
        token["is_staff"] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(
            self.user
        ).data

        return data

class PermissionSerializer(serializers.ModelSerializer):

    app_label = serializers.CharField(
        source="content_type.app_label",
        read_only=True,
    )

    model = serializers.CharField(
        source="content_type.model",
        read_only=True,
    )

    class Meta:
        model = Permission

        fields = [
            "id",
            "name",
            "codename",
            "app_label",
            "model",
        ]

class RoleSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Group

        fields = [
            "id",
            "name",
            "permissions",
        ]

class AdminUserSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()

    role_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        source="groups",
        write_only=True,
        required=False,
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_staff",
            "is_active",
            "roles",
            "role_ids",
            "date_joined",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "date_joined",
            "created_at",
            "is_staff",
        ]

    def get_roles(self, obj):

        return [
            {
                "id": group.id,
                "name": group.name,
            }
            for group in obj.groups.all()
        ]