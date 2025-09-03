from rest_framework import serializers

from apps.sessions.models import SessionModel, SessionPriceModel


class SessionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPriceModel
        fields = ("id", "seat_type", "price")


class SessionSerializer(serializers.ModelSerializer):
    prices = SessionPriceSerializer(many=True)  # вкладені ціни

    class Meta:
        model = SessionModel
        fields = ("id", "movie", "hall", "start_time", "end_time", "prices")

    def create(self, validated_data):
        prices_data = validated_data.pop("prices")  # витягуємо вкладені ціни
        session = SessionModel.objects.create(**validated_data)
        for price_data in prices_data:
            SessionPriceModel.objects.create(session=session, **price_data)
        return session