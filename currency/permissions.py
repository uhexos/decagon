from rest_framework import permissions
from .models import Profile
class HasProfilePermission(permissions.BasePermission):
    message = 'Make a profile to continue.'

    def has_permission(self, request, view):
        return  Profile.objects.filter(user = request.user).exists()