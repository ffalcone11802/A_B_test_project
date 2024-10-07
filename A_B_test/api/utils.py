from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from A_B_test.models import ModelAssignment


def set_session_data(request, user):
    # Set user-specific data in the session
    # Set user id ...
    request.session['user_id'] = user.id
    try:
        model = ModelAssignment.objects.get(user=user.id)
    except ObjectDoesNotExist:
        pass
    else:
        # ... and also model assigned, to facilitate views display on the frontend
        request.session['model'] = model.recommendations_model
    request.session.save()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read and write permissions are only allowed to the owner of the object
        # (only for user profile)
        return bool(request.user and (request.user.is_staff or obj.id == request.user.id))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.id == request.user.id
