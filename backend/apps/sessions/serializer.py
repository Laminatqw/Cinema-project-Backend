from rest_framework import serializers

from apps.sessions.models import SessionModel, SessionPriceModel


class SessionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPriceModel
        fields = ("id", "session", "seat_type", "price")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не може бути від'ємною")
        if value > 10000:
            raise serializers.ValidationError("Ціна не може перевищувати 10000")
        return value

    def validate_seat_type(self, value):
        valid_types = ['regular', 'vip', 'disabled']
        if value not in valid_types:
            raise serializers.ValidationError(f"Тип місця має бути одним з: {', '.join(valid_types)}")
        return value

    def validate(self, data):
        session = data.get('session')
        seat_type = data.get('seat_type')
        if session and seat_type:
            qs = SessionPriceModel.objects.filter(session=session, seat_type=seat_type)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    f"Ціна для типу місця '{seat_type}' вже існує для цієї сесії"
                )
        return data


class SessionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(read_only=True)
    prices = SessionPriceSerializer(many=True, required=False, default=[])
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionModel
        fields = ("id", "movie", "hall", "start_time", "end_time", "prices", "is_active", "status")

    def get_is_active(self, obj):
        from django.utils.timezone import now
        if obj.end_time and obj.end_time < now():
            return False
        return True

    def get_status(self, obj):
        from django.utils.timezone import now
        current = now()
        if obj.start_time and obj.end_time:
            if current < obj.start_time:
                return 'upcoming'
            elif obj.start_time <= current <= obj.end_time:
                return 'active'
            else:
                return 'finished'
        return 'unknown'

    def validate_start_time(self, value):
        from django.utils.timezone import now
        if value < now():
            raise serializers.ValidationError("Час початку не може бути в минулому")
        return value

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        movie = data.get('movie')
        hall = data.get('hall')

        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError(
                    {"end_time": "Час закінчення має бути після часу початку"}
                )
            # перевіряємо мінімальну тривалість — 15 хвилин
            duration = (end_time - start_time).total_seconds() / 60
            if duration < 15:
                raise serializers.ValidationError(
                    {"end_time": "Тривалість сесії має бути щонайменше 15 хвилин"}
                )

        # перевіряємо чи зал не зайнятий в цей час
        if hall and start_time and end_time:
            qs = SessionModel.objects.filter(
                hall=hall,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"hall": "Зал вже зайнятий в цей час"}
                )

        return data

    def create(self, validated_data):
        prices_data = validated_data.pop("prices", [])
        session = SessionModel.objects.create(**validated_data)
        for price_data in prices_data:
            SessionPriceModel.objects.create(session=session, **price_data)
        return session

    def update(self, instance, validated_data):
        prices_data = validated_data.pop("prices", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if prices_data is not None:
            instance.prices.all().delete()
            for price_data in prices_data:
                SessionPriceModel.objects.create(session=instance, **price_data)
        return instance