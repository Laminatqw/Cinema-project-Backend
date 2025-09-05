from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from qr_code import qrcode

from apps import sessions
from apps.tickets.models import TicketModel
from apps.tickets.serializer import TicketSerializer

# Create your views here.

class TicketsListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = TicketModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TicketsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = TicketModel.objects.all()

    def get_queryset(self):
        return TicketModel.objects.filter(user=self.request.user)



def ticket_qr_view(request, pk):
    ticket = get_object_or_404(TicketModel, pk=pk)

    # Дані для QR
    qr_data = f"Ticket ID: {ticket.id} | Session: {ticket.session_id} | Seat: {ticket.seat_id},"

    # Генеруємо QR-код як PNG
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)


    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")