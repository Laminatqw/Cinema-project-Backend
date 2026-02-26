from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.services.email_services import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.auth.serializers import EmailSerializer, PasswordSerializer
from apps.users.models import UserModel
from apps.users.serializers import UserSerializer

# Create your views here.

class ActivateUserView(GenericAPIView):
    """
    patch:
        changes user status "active = 1"
    """

    permission_classes = (AllowAny,)



    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecoveryPasswordRequestView(GenericAPIView):
    """
    post:
        makes request by email for changing password, sends mail with link and token

    """

    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer




    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_password(user)
        return Response(status=status.HTTP_200_OK)


class RecoveryPasswordView(GenericAPIView):
    """
    post:
        after getting token user can change password
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer


    
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({"detail": "Your password has been reset."}, status=status.HTTP_200_OK)

