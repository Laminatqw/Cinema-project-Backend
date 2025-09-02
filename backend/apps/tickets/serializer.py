from django.urls import reverse

from rest_framework import serializers

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