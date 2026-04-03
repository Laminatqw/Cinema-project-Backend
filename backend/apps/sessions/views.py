from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.response import Response

from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from apps.halls.models import HallSeatModel
from apps.sessions.filters import SessionFilter
from apps.sessions.models import SessionModel, SessionPriceModel
from apps.sessions.serializer import SessionSerializer, SessionPriceSerializer
from apps.tickets.models import TicketModel


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
    permission_classes = (IsAdminUser,)

    filterset_class = SessionFilter

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



class SessionPriceListView(ListCreateAPIView):


    """

    get:
        returns prices of session by session id
    post:
        create price for session by session id
    """


    serializer_class = SessionPriceSerializer

    def get_queryset(self):
        session_id = self.kwargs.get("session_id")
        return SessionPriceModel.objects.filter(session_id=session_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SessionPriceDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionPriceSerializer
    queryset = SessionPriceModel.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SessionSeatsView(APIView):
    """
        get:
            returns all seats for session with their availability
        """

    permission_classes = [permissions.AllowAny]

    def get(self, request, session_id):
        session = get_object_or_404(SessionModel, id=session_id)

        if session.end_time and session.end_time < now():
            return Response({"error": "Сесія вже завершена"}, status=status.HTTP_400_BAD_REQUEST)

        seats = HallSeatModel.objects.filter(hall=session.hall)

        taken_seat_ids = TicketModel.objects.filter(
            session=session,
            status__in=['reserved', 'paid']
        ).values_list('seat_id', flat=True)

        data = [
            {
                'id': seat.id,
                'row': seat.row,
                'number': seat.number,
                'seat_type': seat.seat_type,
                'is_taken': seat.id in taken_seat_ids
            }
            for seat in seats
        ]

        return Response(data)
