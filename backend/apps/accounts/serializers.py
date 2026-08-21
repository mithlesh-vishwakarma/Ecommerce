from rest_framework import serializers
from .models import User, Address
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# ==========================================
# USER SERIALIZER
# ==========================================
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to convert User model instances into JSON format and vice versa.
    Exposes public and profile information of a user while marking system fields as read-only.
    """
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
        # These fields cannot be modified directly via user updates
        read_only_fields = [
            "id",
            "is_customer",
            "is_staff",
            "is_active",
            "date_joined",
            "created_at",
        ]


# ==========================================
# ADDRESS SERIALIZER
# ==========================================
class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for managing shipping and billing addresses for users.
    Handles field formatting, database mapping, and auto-populated fields.
    """
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


# ==========================================
# REGISTER SERIALIZER
# ==========================================
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used specifically for User Registration.
    Includes password validation, email duplicate checks, and user object creation.
    """
    # Write-only fields mean passwords are accepted during POST, but never returned in JSON responses
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
        """
        Validates that the email is unique and formatted in lowercase.
        """
        value = value.lower().strip()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):
        """
        Ensures password and confirmation password match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        """
        Creates and returns a new User instance using Django's create_user method (which handles password hashing).
        """
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user


# ==========================================
# PROFILE UPDATE SERIALIZER
# ==========================================
class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used by authenticated users to update their personal details (name, phone, profile image).
    """
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "profile_image",
        ]


# ==========================================
# CHANGE PASSWORD SERIALIZER
# ==========================================
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to handle changing user passwords securely.
    Requires current password and new password confirmation.
    """
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
        """
        Validates that new password and repeat new password match.
        """
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({
                "new_password": "Passwords do not match."
            })

        return attrs


# ==========================================
# LOGIN SERIALIZER (JWT)
# ==========================================
class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Login Serializer that adds custom claims (user_id, email, is_staff) to the JWT payload
    and attaches user details in the authentication response.
    """
    @classmethod
    def get_token(cls, user):
        """
        Adds custom user details to the JWT Token payload.
        """
        token = super().get_token(user)

        token["user_id"] = user.id
        token["email"] = user.email
        token["is_staff"] = user.is_staff

        return token

    def validate(self, attrs):
        """
        Validates credentials and embeds User object details in the API response.
        """
        data = super().validate(attrs)

        data["user"] = UserSerializer(
            self.user
        ).data

        return data


# ==========================================
# PERMISSION & ROLE SERIALIZERS (ADMIN)
# ==========================================
class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Django permissions, showing app name, model, name, and codename.
    """
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
    """
    Serializer for User Groups (Roles), including associated permissions.
    """
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
    """
    Serializer for SuperAdmins to manage staff members and assign user roles (groups).
    """
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
        """
        Returns a simplified list of roles (groups) assigned to the user.
        """
        return [
            {
                "id": group.id,
                "name": group.name,
            }
            for group in obj.groups.all()
        ]