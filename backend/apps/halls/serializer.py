from rest_framework import serializers

from apps.halls.models import HallModel, HallSeatModel


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallModel
        fields = ('id', 'title', 'total_seats', 'hall_type')

    def validate_total_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("Кількість місць має бути більше 0")
        if value > 1000:
            raise serializers.ValidationError("Кількість місць не може перевищувати 1000")
        return value

    def validate_hall_type(self, value):
        valid_types = ['standard', 'imax', '3d']
        if value not in valid_types:
            raise serializers.ValidationError(f"Тип залу має бути одним з: {', '.join(valid_types)}")
        return value

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Назва залу має містити щонайменше 2 символи")
        return value


class HallSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallSeatModel
        fields = ('id', 'hall', 'row', 'number', 'seat_type')

    def validate_row(self, value):
        if value <= 0:
            raise serializers.ValidationError("Номер ряду має бути більше 0")
        return value

    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Номер місця має бути більше 0")
        return value

    def validate_seat_type(self, value):
        valid_types = ['regular', 'vip', 'disabled']
        if value not in valid_types:
            raise serializers.ValidationError(f"Тип місця має бути одним з: {', '.join(valid_types)}")
        return value

    def validate(self, data):
        hall = data.get('hall')
        row = data.get('row')
        number = data.get('number')

        if hall and row and number:
            instance = self.instance
            qs = HallSeatModel.objects.filter(hall=hall, row=row, number=number)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    f"Місце в ряду {row}, номер {number} вже існує в цьому залі"
                )
        return data
