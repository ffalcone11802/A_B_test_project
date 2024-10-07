from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_routes),

    path("items/", views.ItemView.as_view()),
    path("items/<str:pk>", views.ItemRetrieveView.as_view()),

    # path("rating/<str:pk>"),
    # path("recommendations/"),

    path("users/", views.UserListView.as_view()),
    path("users/<str:pk>", views.UserView.as_view()),

    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view())
]
