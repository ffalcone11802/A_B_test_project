from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("", views.get_routes),

    # Test routes
    # activates / deactivates a test by making / clearing users randomization
    path("test/", views.TestView.as_view()),
    # variants management
    path("test/variants/", views.VariantView.as_view()),
    path("test/variants/<str:pk>", views.VariantUpdateView.as_view()),

    path("items/", views.ItemView.as_view()),
    path("items/<str:pk>", views.ItemRetrieveView.as_view()),

    path("users/<str:pk>", views.UserView.as_view()),

    # Login route
    # returns a refresh_jwt and an access_jwt after a post request with the right credentials
    path("token/", jwt_views.TokenObtainPairView.as_view()),

    # Refresh token route
    # returns a new access_jwt after a post request with a valid refresh_jwt
    path("token/refresh/", jwt_views.TokenRefreshView.as_view()),

    # Logout route
    # put the provided refresh_jwt in the token black list
    path("logout/", jwt_views.TokenBlacklistView.as_view()),
]
