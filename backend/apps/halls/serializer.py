from rest_framework import serializers

from apps.halls.models import HallModel, HallSeatModel


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallModel
        fields = ('id', 'title', 'total_seats', 'hall_type')

class HallSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallSeatModel
        fields = ( 'id', 'hall', 'row','number', 'seat_type')
