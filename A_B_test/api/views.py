from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from A_B_test.api.serializers import UserSerializer, ItemSerializer, VariantSerializer
from A_B_test.api.utils import IsOwnerOrReadOnly
from A_B_test.models import Item, Variant
from A_B_test.utils import assign_models, clear_assignments


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
        '*GET /api/test/variants/',
        '*GET /api/test/variants/:id',
        '*GET /api/users/:id',
        'POST /api/token/',
        '*POST /api/token/refresh',
        '*POST /api/logout/',
        '*POST /api/variants/',
        '*PUT /api/test/variants/:id',
        '*PATCH /api/test/variants/:id',
        '*PATCH /api/test/',
        '*DELETE /api/test/',
        '*DELETE /api/variants/:id',
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
        return self.request.user


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


class VariantView(ListCreateAPIView):
    """
    View to get the list of all available variants or to create a new one
    Allowed methods: GET, POST
    """
    serializer_class = VariantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        return Variant.objects.all()


class VariantUpdateView(RetrieveUpdateDestroyAPIView):
    """
    View to get, update, modify or delete a variant
    Allowed methods: GET, PUT, PATCH, DELETE
    """
    serializer_class = VariantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['pk']
        return Variant.objects.filter(id=room_id)


class TestView(GenericAPIView):
    """
    View to activate or deactivate a test
    Allowed methods: PATCH, DELETE
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    @staticmethod
    def patch(request):
        assign_models()

    @staticmethod
    def delete(request):
        clear_assignments()
