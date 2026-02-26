from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import qrcode

from apps import sessions
from apps.tickets.models import TicketModel
from apps.tickets.serializer import TicketDetailSerializer, TicketSerializer

# Create your views here.

class TicketsListView(ListCreateAPIView):

    """
    get:
        shows user only his tickets(if not staff)
    post:
        creates ticket(for authenticated user)
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = TicketModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user)

class TicketsDetailView(RetrieveUpdateDestroyAPIView):

    """
    get:
        shows authenticated user detailed info about his ticket, by id
    patch:
        edits ticket info by id(only for staff)
    delete:
        deletes ticket by id(only for staff)
    """

    serializer_class = TicketSerializer
    queryset = TicketModel.objects.all()

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class TicketQRView(APIView):

    """
    get:
        returns qr-code of ticket by uuid
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TicketDetailSerializer

    def get(self, request, uuid):
        ticket = get_object_or_404(TicketModel, uuid=uuid, user=request.user)

        # QR містить тільки id квитка
        qr_data = uuid

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer, content_type="image/png")


class TicketValidateView(APIView):

    """
    post:
        checks if ticket is valid, if true changes is to used
    """

    permission_classes = (IsAdminUser,)

    def post(self, request):
        uuid = request.data.get("uuid")
        ticket = get_object_or_404(TicketModel, uuid=uuid)

        # Перевірки
        if ticket.status == "used":
            return Response({"valid": False, "reason": "Квиток вже використаний"}, status=400)

        if ticket.session.start_time < timezone.now() < ticket.session.end_time:
            # Маркуємо як використаний
            ticket.status = "used"
            ticket.save()
            return Response({"valid":True,
                             "reason":"Квиток провалідовано",
                            "ticket_id": ticket.id,
                            "movie": ticket.session.movie.name,
                            "hall": ticket.seat.hall.title,
                            "row": ticket.seat.row,
                            "seat": ticket.seat.number,
                            "time": ticket.session.start_time}, status=200)

        elif ticket.session.start_time > timezone.now():
            return Response({"valid": False, "reason": "Сеанс ще не почався"}, status=400)

        else:
            return Response({"valid":False, "reason": "Сеанс вже закінчився"}, status=400)




