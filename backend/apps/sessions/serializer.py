from rest_framework import serializers

from apps.sessions.models import SessionModel


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionModel
        fields = ('movie','hall','start_time','end_time','price')