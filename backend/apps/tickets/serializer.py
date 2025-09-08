from io import BytesIO

from django.core.files import File

from rest_framework import serializers

import qrcode

from apps.tickets.models import TicketModel


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketModel
        fields = ('user','session','seat','status')


    def get_qr_code_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/tickets/{obj.pk}/qr/")
        return f"/api/tickets/{obj.pk}/qr/"

    def create(self, validated_data):
        ticket = super().create(validated_data)
        return ticket

class TicketDetailSerializer(serializers.ModelSerializer):
    # з seat
    hall = serializers.CharField(source="seat.hall.title")
    row = serializers.IntegerField(source="seat.row")
    number = serializers.IntegerField(source="seat.number")
    seat_type = serializers.CharField(source="seat.seat_type")

    # з session → movie
    movie = serializers.CharField(source="session.movie.name")
    start_time = serializers.DateTimeField(source="session.start_time")

    class Meta:
        model = TicketModel
        fields = (
            "id",
            "status",
            "hall",
            "row",
            "number",
            "seat_type",
            "movie",
            "start_time",
        )
