from rest_framework import serializers

from apps.movies.models import GenreModel, MovieModel


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = ('id', 'genre_name',)

    def validate_genre_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Назва жанру має містити щонайменше 2 символи")
        # перевірка унікальності
        qs = GenreModel.objects.filter(genre_name__iexact=value.strip())
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Жанр з такою назвою вже існує")
        return value.strip()


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=GenreModel.objects.all()
    )
    genres_detail = GenreSerializer(source="genres", many=True, read_only=True)
    is_now_showing = serializers.SerializerMethodField()

    class Meta:
        model = MovieModel
        fields = ('id', 'name', 'length',
                  'picture', 'trailer_link',
                  'rating', 'genres', 'genres_detail',
                  'year', 'is_now_showing',
                  'release_date', 'end_date')

    def get_is_now_showing(self, obj):
        return obj.is_now_showing

    def validate_name(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Назва фільму не може бути порожньою")
        return value.strip()

    def validate_length(self, value):
        if value <= 0:
            raise serializers.ValidationError("Тривалість фільму має бути більше 0 хвилин")
        if value > 600:
            raise serializers.ValidationError("Тривалість фільму не може перевищувати 600 хвилин")
        return value

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Рейтинг має бути від 0 до 10")
        return value

    def validate_year(self, value):
        from django.utils.timezone import now
        current_year = now().year
        if value < 1888:
            raise serializers.ValidationError("Рік не може бути раніше 1888")
        if value > current_year + 5:
            raise serializers.ValidationError(f"Рік не може бути більше {current_year + 5}")
        return value

    def validate_trailer_link(self, value):
        if value and not (value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError("Посилання має починатись з http:// або https://")
        return value

    def validate(self, data):
        release_date = data.get('release_date')
        end_date = data.get('end_date')
        if release_date and end_date and end_date < release_date:
            raise serializers.ValidationError(
                {"end_date": "Дата завершення не може бути раніше дати виходу"}
            )
        return data

    def create(self, validated_data):
        genres = validated_data.pop("genres", [])
        movie = MovieModel.objects.create(**validated_data)
        if genres:
            movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop("genres", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if genres is not None:
            instance.genres.set(genres)
        return instance


class MoviePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ('picture',)
        extra_kwargs = {'picture': {'required': True}}

    def validate_picture(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("Розмір постера не може перевищувати 5MB")
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Постер має бути у форматі JPEG, PNG або WebP")
        return value