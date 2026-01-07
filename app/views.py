from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import ( CreateUserSerializer, UserListSerializer, UserUpdateSerializer, MeSerializer )
from .permissions import IsAdmin, IsAdminOrManager ,IsAnyAuthenticated

User = get_user_model()



class UserListCreateView(APIView):
    permission_classes = [IsAdminOrManager]

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.role.name != "admin":
            return Response(
                {"detail": "Only admin can create users"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )


class UserDetailView(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User updated successfully"})

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class MeView(APIView):
    permission_classes = [IsAnyAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
