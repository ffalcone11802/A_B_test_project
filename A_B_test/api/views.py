from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from A_B_test.api.serializers import *
from A_B_test.api.utils import *
from A_B_test.models import User, VariantAssignment
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
        'NI api/recommendations/  GET',
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
    serializer_class = VariantAssignmentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    recommendations_data = []

    def get_queryset(self):
        return self.request.GET.get('page')

    def get(self, request, *args, **kwargs):
        recs = self.get_recommendations(request)
        print(recs)
        """token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZDAzMjgxYmY1ZjExNWMxNTM4Mzk3ZTcyM2NhMWFmOCIsIm5iZiI6MTczMDU0NTA3OS44NDQyMTgsInN1YiI6IjY3MjYwMzAzYWM4YjQ4MTllNWYwNTNkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jjeX6EsboH8aObL6ExDI7ssVtGbfsqmSd34xx_jE6uM'
        language = 'en-US'

        response = requests.get("https://api.themoviedb.org/3/movie/popular",
                                params={'page': self.get_queryset(),
                                        'language': language},
                                headers={'Authorization': f'Bearer {token}'})
        response = response.json()
        f = open('datasets/Nuovo Documento di testo.txt', 'a')
        for item in response['results']:
            f.write(str(item['id']) + '\n')
        f.close()"""

        # beautifying and printing the JSON response
        # return Response(response.json())
        return Response({'detail': 'Recs written'})
