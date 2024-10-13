from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from A_B_test.api.serializers import UserSerializer, ItemSerializer, VariantSerializer, VariantAssignmentSerializer, RegisterSerializer
from A_B_test.api.utils import read_from_csv, IsManagerOrReadOnly, IsOwner, IsManager, TestUtils, SessionUtils
from A_B_test.models import Item, User, Variant, VariantAssignment
from django.contrib.auth import authenticate


@api_view(['GET'])
def get_routes(request):
    """
    Function to get a list of all the available APIs
    (* = authentication credentials required)
    (** = manager role required)
    """
    routes = [
        'api/  GET',
        'api/users/  POST'
        'api/users/:id/  *GET *PUT *PATCH *DELETE',
        'api/login/  POST',
        'api/logout/  *GET',
        'api/recommendations/  GET',
        'api/items/  *GET **POST',
        'api/items/:id/  *GET **PUT **PATCH **DELETE',
        'api/test/assign-models/  **GET',
        'api/test/variants/  **GET **POST',
        'api/test/variants/:id/  **GET **PUT **PATCH **DELETE'
    ]
    return Response(routes)


class LoginView(APIView, SessionUtils):
    """
    View to handle user login
    Allowed methods: POST
    """
    def __init__(self):
        super().__init__()

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        self._user = authenticate(request, username=username, password=password)
        return self.do_login(request)


class LogoutView(APIView, SessionUtils):
    """
    View to handle user logout
    Allowed methods: GET
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()

    def get(self, request):
        return self.do_logout(request)


class UserView(CreateAPIView):
    """
    View to create a new user profile
    Allowed methods: POST
    """
    serializer_class = RegisterSerializer


class UserManagementView(RetrieveUpdateDestroyAPIView):
    """
    View to manage a specific user profile
    Allowed methods: GET, PUT, PATCH, DELETE
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)


class ItemView(ListCreateAPIView):
    """
    View to get all the items available or to create a new one
    Allowed methods: GET, POST
    """
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]

    def get_queryset(self):
        return Item.objects.all()


class ItemManagementView(RetrieveUpdateDestroyAPIView):
    """
    View to manage a specific item
    Allowed methods: GET, PUT, PATCH, DELETE
    """
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]

    def get_queryset(self):
        item_id = self.kwargs['pk']
        return Item.objects.filter(id=item_id)


class VariantView(ListCreateAPIView):
    """
    View to list all the available test variants or to create a new one
    Allowed methods: GET, POST
    """
    serializer_class = VariantSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return Variant.objects.all()


class VariantManagementView(RetrieveUpdateDestroyAPIView):
    """
    View to manage a specific test variant
    Allowed methods: GET, PUT, PATCH, DELETE
    """
    serializer_class = VariantSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        var_id = self.kwargs['pk']
        return Variant.objects.filter(id=var_id)


class AssignmentsView(ListCreateAPIView, DestroyAPIView, TestUtils):
    """
    View to perform models assignment and to clear it
    Allowed methods: GET, POST, DELETE
    """
    serializer_class = VariantAssignmentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def __init__(self):
        super().__init__()

    def get_queryset(self):
        return VariantAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        users_list = User.objects.filter(is_superuser=False, is_manager=False, is_active=True)
        self.assign_models(users_list)

        # Retrieve assignments list
        assignments_list = VariantAssignment.objects.all()
        serializer = self.get_serializer(data=assignments_list, many=True)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        assignments = VariantAssignment.objects.all()
        for asg in assignments:
            self.perform_destroy(asg)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendationsView(ListAPIView, TestUtils):
    """
    View to retrieve recommendations produced by models
    Allowed methods: GET
    """
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    recommendations_data = []

    def get_queryset(self):
        return Item.objects.filter(id__in=self.recommendations_data)

    def get(self, request, *args, **kwargs):
        self.send_request_to_model(request)
        self.recommendations_data = read_from_csv('recommendations.csv')
        return self.list(request, *args, **kwargs)
