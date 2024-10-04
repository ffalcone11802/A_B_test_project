from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from A_B_test.api.serializers import UserSerializer, ItemSerializer
from A_B_test.api.utils import IsOwnerOrReadOnly
from A_B_test.models import Item, User


@api_view(['GET'])
def get_routes(request):
    """
    Function to get a list of all the available APIs
    (* = authentication credentials or refresh_token required)
    """
    routes = [
        'GET /api/',
        'GET /api/items/',
        'GET /api/items/:id',
        '*GET /api/users/:id',
        'POST /api/token/',
        '*POST /api/token/refresh',
        '*POST /api/logout/'
    ]
    return Response(routes)


class UserView(RetrieveAPIView):
    """
    View to get user information
    Allowed methods: GET
    """
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)


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
