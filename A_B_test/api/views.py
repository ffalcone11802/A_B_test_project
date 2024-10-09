from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from A_B_test.api.serializers import UserSerializer, ItemSerializer
from A_B_test.api.utils import set_session_data, IsOwnerOrAdmin, read_from_csv
from A_B_test.models import Item, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session

from A_B_test.test.test_utils import send_request_to_model


@api_view(['GET'])
def get_routes(request):
    """
    Function to get a list of all the available APIs
    (* = authentication credentials required)
    """
    routes = [
        'GET /api/',
        'GET /api/items/',
        'GET /api/items/:id',
        '*GET /api/users/',
        '*GET /api/users/:id',
        'POST /api/login/',
        '*GET /api/logout/'
    ]
    return Response(routes)


class UserListView(ListAPIView):
    """
    View to get the list of all the available users
    Allowed methods: GET
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return User.objects.all()


class UserView(RetrieveAPIView):
    """
    View to get user information
    Allowed methods: GET
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)


class LoginView(APIView):
    """
    View to handle user login
    Allowed methods: POST
    """
    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            set_session_data(request, user)
            return Response({'detail': 'Successfully logged in'})
        else:
            return Response({'detail': 'No active account found with the given credentials'})


class LogoutView(APIView):
    """
    View to handle user logout
    Allowed methods: GET
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        logout(request)
        # Clear user's session data
        Session.objects.filter(session_key=request.session.session_key).delete()
        return Response({'detail': 'Successfully logged out'})


class ItemView(ListAPIView):
    """
    View to get all the items available
    Allowed methods: GET
    """
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.all()


class ItemRetrieveView(RetrieveAPIView):
    """
    View to retrieve a specific item
    Allowed methods: GET
    """
    serializer_class = ItemSerializer

    def get_queryset(self):
        item_id = self.kwargs['pk']
        return Item.objects.filter(id=item_id)


class RecommendationsView(ListAPIView):
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
        send_request_to_model(request)
        self.recommendations_data = read_from_csv('recommendations.csv')
        return self.list(request, *args, **kwargs)
