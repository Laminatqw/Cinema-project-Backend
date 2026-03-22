from django.shortcuts import render
from django.utils.timezone import now

from rest_framework import permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from apps.sessions.models import SessionModel
from apps.sessions.serializer import SessionSerializer

# Create your views here.

class SessionListView(ListCreateAPIView):

    """
    get:
        shows all sessions(for anyone)
    post:
        creates session(for staff)
    """

    serializer_class = SessionSerializer
    queryset = SessionModel.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return SessionModel.objects.all()
        return SessionModel.objects.filter(end_time__gte=now())

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SessionDetailView(RetrieveUpdateDestroyAPIView):

    """
    get:
        show session by id(for anyone)
    patch:
        edits session info by id(for staff)
    delete:
        deletes session by id(for staff)
    """


    serializer_class = SessionSerializer
    queryset = SessionModel.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]