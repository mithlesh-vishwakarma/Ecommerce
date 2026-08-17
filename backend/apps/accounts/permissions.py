from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Only Django superusers can manage staff roles.
    """

    message = (
        "Only the Super Admin can manage roles "
        "and staff permissions."
    )

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class HasModelPermission(BasePermission):
    """
    Check Django's model permissions based on
    the HTTP method.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        # Superuser gets everything
        if request.user.is_superuser:
            return True

        model = view.queryset.model

        if request.method == "GET":
            action = "view"

        elif request.method == "POST":
            action = "add"

        elif request.method in ["PUT", "PATCH"]:
            action = "change"

        elif request.method == "DELETE":
            action = "delete"

        else:
            return False

        permission_name = (
            f"{model._meta.app_label}."
            f"{action}_"
            f"{model._meta.model_name}"
        )

        return request.user.has_perm(permission_name)