from rest_framework import permissions

from apps.user.services.constants import MENTOR


class AllowMentor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_mentor and request.user.user_type == MENTOR:
                return True
