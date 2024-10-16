from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_routes),

    path("users/", views.UserView.as_view()),
    path("users/<str:pk>", views.UserManagementView.as_view()),

    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),

    # path("rating/<str:pk>"),
    path("recommendations/", views.RecommendationsView.as_view()),

    path("items/", views.ItemView.as_view()),
    path("items/<str:pk>", views.ItemManagementView.as_view()),

    path("test/assignments/", views.AssignmentsView.as_view()),
    path("test/variants/", views.VariantView.as_view()),
    path("test/variants/<str:pk>", views.VariantManagementView.as_view())
]
