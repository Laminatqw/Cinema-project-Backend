from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from rest_framework import serializers

from core.services.email_services import EmailService

from apps.users.models import ProfileModel

# from core.services.email_service import EmailService

UserModel = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'created_at', 'updated_at')

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Ім'я має містити щонайменше 2 символи")
        if not value.strip().isalpha():
            raise serializers.ValidationError("Ім'я має містити тільки літери")
        return value.strip()

    def validate_surname(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Прізвище має містити щонайменше 2 символи")
        if value and not value.strip().isalpha():
            raise serializers.ValidationError("Прізвище має містити тільки літери")
        return value.strip() if value else value

    def validate_age(self, value):
        if value is not None:
            if value < 1:
                raise serializers.ValidationError("Вік не може бути менше 1")
            if value > 120:
                raise serializers.ValidationError("Вік не може перевищувати 120")
        return value


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            'id', 'email', 'password', 'is_active', 'is_staff',
            'is_superuser', 'last_login', 'created_at', 'updated_at', 'profile',
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        qs = UserModel.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Користувач з таким email вже існує")
        return value.lower()

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль має містити щонайменше 8 символів")
        if value.isdigit():
            raise serializers.ValidationError("Пароль не може складатись тільки з цифр")
        if value.isalpha():
            raise serializers.ValidationError("Пароль має містити щонайменше одну цифру")
        return value

    @atomic
    def create(self, validated_data: dict):
        profile_data = validated_data.pop('profile', None)
        user = UserModel.objects.create_user(**validated_data)
        validated_data['is_active'] = True
        if profile_data:
            ProfileModel.objects.create(user=user, **profile_data)
        EmailService.register(user)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance