from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from A_B_test.api.serializers import *
from A_B_test.api.utils import *
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
        'api/users/:id/  *GET *PATCH *DELETE',
        'api/login/  POST',
        'api/logout/  *GET',
        'api/recommendations/  GET',
        'api/items/  *GET **POST',
        'api/items/:id/  *GET **PATCH **DELETE',
        'api/test/assignments/  **GET **POST **DELETE',
        'api/test/variants/  **GET **POST',
        'api/test/variants/:id/  **GET **PATCH **DELETE'
    ]
    return Response(routes)


class LoginView(APIView, SessionUtils):
    """
    View to handle user login
    Allowed methods: POST
    """

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

    def get(self, request):
        return self.do_logout(request)


class UserView(CreateAPIView):
    """
    View to create a new user profile
    Allowed methods: POST
    """
    serializer_class = RegisterSerializer


class UserManagementView(CustomRetrieveUpdateDestroyAPIView):
    """
    View to manage a specific user profile
    Allowed methods: GET, PATCH, DELETE
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    _allowed_fields = ['first_name', 'last_name', 'password', 'is_active']

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


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


class ItemManagementView(CustomRetrieveUpdateDestroyAPIView):
    """
    View to manage a specific item
    Allowed methods: GET, PATCH, DELETE
    """
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    _allowed_fields = ['title', 'description']

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


class VariantManagementView(CustomRetrieveUpdateDestroyAPIView):
    """
    View to manage a specific test variant
    Allowed methods: GET, PATCH, DELETE
    """
    serializer_class = VariantSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsManager]
    _allowed_fields = ['name', 'endpoint']

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

    def get_queryset(self):
        return VariantAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        users_list = User.objects.filter(is_superuser=False, is_staff=False, is_manager=False, is_active=True)
        if len(users_list):
            self.assign_models(users_list)
            return Response(
                {'detail': 'Assignment successfully performed or updated'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'detail': 'No users found'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        assignments = VariantAssignment.objects.all()
        for asg in assignments:
            self.perform_destroy(asg)
        return Response(
            {'detail': 'Assignment successfully cleared'},
            status=status.HTTP_204_NO_CONTENT
        )


class RecommendationsView(ListCreateAPIView, TestUtils):
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
