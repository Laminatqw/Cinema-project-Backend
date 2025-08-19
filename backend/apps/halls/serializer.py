from rest_framework import serializers

from apps.halls.models import HallModel


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallModel
        fields = ('title', 'total_seats', 'hall_type')