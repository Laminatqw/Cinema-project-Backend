from django.shortcuts import render

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.sessions.models import SessionModel
from apps.sessions.serializer import SessionSerializer

# Create your views here.

class SessionListView(ListCreateAPIView):
        permission_classes = (IsAdminUser,)
        serializer_class = SessionSerializer
        queryset = SessionModel.objects.all()

class SessionDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SessionSerializer
    queryset = SessionModel.objects.all()