from rest_framework import permissions
from .models import Profile,Fund,Withdrawal
from django.shortcuts import get_object_or_404


class HasProfilePermission(permissions.BasePermission):
    message = 'Make a profile to continue.'

    def has_permission(self, request, view):
        return Profile.objects.filter(user=request.user).exists()


class IsAdmin(permissions.BasePermission):
    message = 'Must be an admin to perform this operation'

    def has_permission(self, request, view):
        return get_object_or_404(Profile, user=request.user.id).role == 'AD'
        # return Profile.objects.get(id=request.user.id).role == "AD"

class CanUpdateProfile(permissions.BasePermission):
    message = 'Must be an admin to update profile' 

    def has_permission(self, request, view):
        if view.action in ['update', 'partial_update']:
            return request.user.profile.role == "AD"
        return True

class CanCreateWallet(permissions.BasePermission):
    message = 'Admin cannot have a wallet' 

    def has_permission(self, request, view):
        if view.action in ['create']:
            return not get_object_or_404(Profile, user=request.user.id).role == 'AD'
        return True
        
class IsElite(permissions.BasePermission):
    message = 'Must be an admin to perform this operation'

    def has_permission(self, request, view):
        return get_object_or_404(Profile, user=request.user.id).role == 'EL'


class IsNoob(permissions.BasePermission):
    message = 'Must be an admin to perform this operation'

    def has_permission(self, request, view):
        return get_object_or_404(Profile, user=request.user.id).role == 'NB'
        # return Profile.objects.get(id=request.user.id).role == "AD"

class IsFundOwner(permissions.BasePermission):
    message = 'Must be the owner or admin to perform this operation'

    def has_permission(self, request, view):
        return get_object_or_404(Fund, id=request.POST.get("fund_id")).to_user == request.user 

class IsWithdrawalOwner(permissions.BasePermission):
    message = 'Must be the owner or admin to perform this operation'

    def has_permission(self, request, view):
        withdrawal = get_object_or_404(Withdrawal, id=request.POST.get("withdrawal_id"))
        return withdrawal.from_user == request.user