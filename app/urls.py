from django.urls import path
from .views import ( UserListCreateView, UserDetailView, MeView )

urlpatterns = [
    path("users/", UserListCreateView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("me/", MeView.as_view()),
]
