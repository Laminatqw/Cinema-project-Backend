from io import BytesIO

from django.core.files import File

from rest_framework import serializers

import qrcode

from apps.tickets.models import TicketModel


class TicketSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = TicketModel
        fields = ('id', 'uuid', 'user', 'session', 'seat', 'status', 'qr_code_url')
        read_only_fields = ('uuid', 'user', 'status')

    def get_qr_code_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/tickets/{obj.uuid}/qr/")
        return f"/api/tickets/{obj.uuid}/qr/"

    def validate(self, data):
        session = data.get('session')
        seat = data.get('seat')

        if session and seat:
            # перевіряємо чи місце належить до залу сесії
            if seat.hall != session.hall:
                raise serializers.ValidationError(
                    {"seat": "Місце не належить до залу цієї сесії"}
                )

            # перевіряємо чи квиток на це місце вже існує
            qs = TicketModel.objects.filter(
                session=session,
                seat=seat,
                status__in=['reserved', 'paid']
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"seat": "Це місце вже заброньовано або оплачено"}
                )

            # перевіряємо чи сесія ще активна або майбутня
            from django.utils.timezone import now
            if session.end_time and session.end_time < now():
                raise serializers.ValidationError(
                    {"session": "Сесія вже завершена"}
                )

        return data

    def create(self, validated_data):
        ticket = super().create(validated_data)
        return ticket


class TicketDetailSerializer(serializers.ModelSerializer):
    hall = serializers.CharField(source="seat.hall.title")
    row = serializers.IntegerField(source="seat.row")
    number = serializers.IntegerField(source="seat.number")
    seat_type = serializers.CharField(source="seat.seat_type")
    movie = serializers.CharField(source="session.movie.name")
    start_time = serializers.DateTimeField(source="session.start_time")

    class Meta:
        model = TicketModel
        fields = (
            "id",
            "uuid",
            "status",
            "hall",
            "row",
            "number",
            "seat_type",
            "movie",
            "start_time",
        )