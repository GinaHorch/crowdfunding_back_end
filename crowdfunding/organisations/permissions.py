from rest_framework import permissions

class IsOrganisationOwner(permissions.BasePermission):
    """
    Custom permission to only allow Organisation Owners (Admins) to access certain views.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Organisation Owners').exists())

class IsOrganisationStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Organisation Staff').exists())

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user