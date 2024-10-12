from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
      if request.method in permissions.SAFE_METHODS:
          return True
      return obj.owner == request.user
    
    # if obj.owner
        # if obj.owner == request.user
        # if obj.owner is not None
    # if obj.supporter 
        # if obj.supporter == request.user

        # return TRUE

class IsSupporterOrReadOnly(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
          return True
        return obj.supporter == request.user