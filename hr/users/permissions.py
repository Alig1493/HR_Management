from rest_framework import permissions

from hr.users.config import Config


class IsHRPermitted(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        permission = super().has_permission(request, view)

        if permission and request.user.role == Config.HR:
            return True

        return False


class IsManagerPermitted(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        permission = super().has_permission(request, view)

        if permission and request.user.role == Config.MANAGER:
            return True

        return False
