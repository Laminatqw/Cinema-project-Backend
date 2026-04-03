from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import qrcode

from apps import sessions
from apps.halls.models import HallSeatModel
from apps.sessions.models import SessionModel
from apps.tickets.models import TicketModel
from apps.tickets.serializer import TicketDetailSerializer, TicketSerializer

# Create your views here.

class TicketsListView(ListCreateAPIView):

    """
        get:
            returns all tickets of specified user
        post:
            creates one or many(bulk) tickets

    """



    permission_classes = (IsAuthenticated,)
    queryset = TicketModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TicketDetailSerializer
        return TicketSerializer

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)

        if many:
            tickets = [
                TicketModel(user=request.user, **ticket)
                for ticket in serializer.validated_data
            ]
            TicketModel.objects.bulk_create(tickets)
            return Response({"created": len(tickets)}, status=status.HTTP_201_CREATED)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketsDetailView(RetrieveUpdateDestroyAPIView):

    """
    get:
        shows authenticated user detailed info about his ticket, by id
    patch:
        edits ticket info by id(only for staff)
    delete:
        deletes ticket by id(only for staff)
    """


    queryset = TicketModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TicketDetailSerializer
        return TicketSerializer
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




# class TicketValidateView(APIView):
#
#     """
#     post:
#         checks if ticket is valid, if true changes is to used
#     """
#
#     permission_classes = (IsAdminUser,)
#
#     def post(self, request):
#         uuid = request.data.get("uuid")
#         ticket = get_object_or_404(TicketModel, uuid=uuid)
#
#         # Перевірки
#         if ticket.status == "used":
#             return Response({"valid": False, "reason": "Квиток вже використаний"}, status=400)
#
#         if ticket.session.start_time < timezone.now() < ticket.session.end_time:
#             # Маркуємо як використаний
#             ticket.status = "used"
#             ticket.save()
#             return Response({"valid":True,
#                              "reason":"Квиток провалідовано",
#                             "ticket_id": ticket.id,
#                             "movie": ticket.session.movie.name,
#                             "hall": ticket.seat.hall.title,
#                             "row": ticket.seat.row,
#                             "seat": ticket.seat.number,
#                             "time": ticket.session.start_time}, status=200)
#
#         elif ticket.session.start_time > timezone.now():
#             return Response({
#                              "ticket_id": ticket.id,
#                              "movie": ticket.session.movie.name,
#                              "hall": ticket.seat.hall.title,
#                              "row": ticket.seat.row,
#                              "seat": ticket.seat.number,
#                              "valid": False, "reason": "Сеанс ще не почався",
#                              "time": ticket.session.start_time}, status=400)
#
#         else:
#             return Response({"valid":False, "reason": "Сеанс вже закінчився"}, status=400)




