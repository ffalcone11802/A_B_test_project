import csv
import os
import pandas as pd
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status, mixins, generics
from rest_framework.response import Response
from A_B_test.models import VariantAssignment
from A_B_test_project.config import variants
from manage import update


class TestUtils:
    """
    Class to group all test utilities
    """

    def assign_models(self, users_list):
        """
        Custom function for users randomization between variants
        """
        # Initializing variant counters
        counter = {}
        for var in variants:
            counter.update({var: 0})

        # Hashing and sorting users' ids
        hash_ids = []
        for user in users_list:
            hash_ids.append({'hash': hash(user.id), 'id': user.id})
        sorted_hash_ids = sorted(hash_ids, key=lambda d: d['hash'])

        # Performing assignment
        for hashed_id, user_id in sorted_hash_ids:
            try:
                asg = VariantAssignment.objects.get(user_id=user_id)
                counter[asg.variant] += 1
            except ObjectDoesNotExist:
                # If user does not have any assignments yet, create it
                var = min(counter, key=counter.get)
                user = next((u for u in users_list if u.id == user_id), None)
                VariantAssignment.objects.create(user=user, variant=var)
                counter[var] += 1
            else:
                pass

    def get_recommendations(self, request):
        if 'variant' in request.session:
            # Getting the assigned model...
            variant = variants[request.session['variant']]
        else:
            # ...or the most popular one
            variant = variants[f'var{len(variants)}']

        recs = self.read_from_tsv(
            os.path.abspath(os.sep.join([update.output_path, f"{variant.name}.tsv"])),
            request.user.id
        )
        return recs

    def read_from_tsv(self, path, user_id):
        recs = []
        with open(path) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for row in tsv_file:
                if row[0] == str(user_id):
                    recs.append(row[1])
        return recs


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
            request.session['variant'] = asg.variant
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
