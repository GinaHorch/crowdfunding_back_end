from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
      if request.method in permissions.SAFE_METHODS:
          return True
      return obj.organisation == request.user
  
class IsSupporterOrReadOnly(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
          return True
        return obj.supporter == request.user