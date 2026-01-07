from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role and
            request.user.role.name in self.allowed_roles
        )


class IsAdmin(BaseRolePermission):
    allowed_roles = ["admin"]


class IsAdminOrManager(BaseRolePermission):
    allowed_roles = ["admin", "manager"]


class IsAnyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


