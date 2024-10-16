import pandas as pd
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status, mixins, generics
from rest_framework.response import Response
from A_B_test.models import VariantAssignment, Item, Variant
from itertools import cycle


class TestUtils:
    """
    Class to group all test utilities
    """
    __variants = Variant.objects.all()

    def assign_models(self, users_list):
        """
        Custom function for users randomization between models
        """
        for user, var in zip(users_list, cycle(self.__variants)):
            try:
                VariantAssignment.objects.get(user_id=user.id)
            except ObjectDoesNotExist:
                # If user does not have any assignments yet, create it
                VariantAssignment.objects.create(user=user, variant=var)
            else:
                pass

    def send_request_to_model(self, request):
        if request.session['model'].exists():
            variant = filter(lambda m: m.name == request.session['model'], self.__variants)
            user_id = request.user.id
            endpoint = variant.endpoint

            # send request to the model endpoint providing user_id
            # (using websocket to wait asynchronously for the response)

        else:
            return Response({'detail': 'No model found'})


def read_from_csv(csv_file):
    """
    Function to read from .csv file and query the db
    :param csv_file: .csv file containing recommendations from the model
    :return: list of the recommended items id
    """
    items_list = []

    with open(csv_file, 'r') as file:
        recommendations = pd.read_csv(file)

        for row in recommendations.iterrows():
            title = row[1]['title']
            # If items does not already exist...
            try:
                item = Item.objects.get(title=title)
            except ObjectDoesNotExist:
                pass
            else:
                items_list.append(item.id)

    return items_list


class SessionUtils:
    """
    Class to group all session management utils
    """
    _user = None

    def do_login(self, request):
        if self._user is not None:
            login(request, self._user)
            self.set_session_data(request)
            return Response({'detail': 'Successfully logged in'})
        else:
            return Response({'detail': 'No active account found with the given credentials'})

    def do_logout(self, request):
        self._user = None
        logout(request)
        # Clear user's session data
        request.session.delete()
        return Response({'detail': 'Successfully logged out'})

    def set_session_data(self, request):
        # Set user-specific data in the session
        # Set user id ...
        request.session['user_id'] = self._user.id
        try:
            asg = VariantAssignment.objects.get(user=self._user.id)
        except ObjectDoesNotExist:
            pass
        else:
            # ... and also assigned variant
            request.session['variant'] = asg.variant.name
        request.session.save()


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow profile owner to view and edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read and write permissions are only allowed to the object owner
        # (only for user profile)
        return bool(request.user and obj.id == request.user.id)


class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow managers to view and edit test variants
    """
    def has_permission(self, request, view):
        # Read and write permissions on test variants are only allowed to the managers of the app
        return bool(request.user.is_manager)


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow managers to edit items
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions on items are only allowed to the managers of the app
        return bool(request.user.is_manager)


class FieldsControl:
    """
    Class to allow user to edit only some object fields
    """
    _allowed_fields = []
    _method = None

    def check_fields(self, request, *args, **kwargs):
        for k in request.POST.keys():
            if k not in self._allowed_fields:
                return Response(
                    {'detail': f'Only these fields are editable: {self._allowed_fields}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return self._method(request, *args, **kwargs)


class CustomRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin,
                                         generics.GenericAPIView,
                                         FieldsControl):
    """
    Custom API view to allow controls on editable fields
    Allow methods: GET, PATCH, DELETE
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self._method = self.partial_update
        return self.check_fields(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
