# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import permissions, status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import UserSerializer

from core.services.email_services import EmailService


UserModel = get_user_model()


class UsersListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UsersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    """
    get:
        shows user info about his account
    patch:
        edits info about users account
    delete:
        deletes user account
    """


    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.request.method in ['GET','PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class RegisterUserView(GenericAPIView):

    """
        post:
            register user
    """

    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            EmailService.register(user)
            return Response(
                {"detail": "User registered successfully.", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    """
        post:
            logout user by refresh token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail":"Successfully logged out."},
                status = status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST
            )