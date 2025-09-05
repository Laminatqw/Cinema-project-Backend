from io import BytesIO

from django.core.files import File
from django.urls import reverse

from rest_framework import serializers

import qrcode

from apps.tickets.models import TicketModel


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketModel
        fields = ('user','session','seat','status','qr_code')


    def get_qr_code_url(self, obj):
        # лінк на спеціальний ендпоінт, що верне QR
        request = self.context.get("request")
        url = reverse("ticket_qr", kwargs={"pk": obj.pk})
        return request.build_absolute_uri(url)

    def create(self, validated_data):
        ticket = super().create(validated_data)

        # Генерація QR-коду
        qr = qrcode.make(f"Ticket ID: {ticket.id}, Session: {ticket.session_id}, Seat: {ticket.seat_id}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Зберігаємо у поле qr_code
        ticket.qr_code.save(f"ticket_{ticket.id}.png", File(buffer), save=False)
        ticket.save()

        return ticket
