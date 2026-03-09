from rest_framework import serializers

from apps.movies.models import GenreModel, MovieModel


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = ('id','genre_name',)


class MovieSerializer(serializers.ModelSerializer):


    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=GenreModel.objects.all()
    )
    # Повертаємо деталі жанрів на читання
    genres_detail = GenreSerializer(source="genres", many=True, read_only=True)

    is_now_showing = serializers.SerializerMethodField()

    class Meta:
        model = MovieModel
        fields = ('id','name', 'length', 'picture', 'trailer_link', 'rating', 'genres', 'genres_detail', 'year', 'is_now_showing')

    def get_is_now_showing(self, obj):
        return obj.is_now_showing

    def create(self, validated_data):
        genres = validated_data.pop("genres", [])
        movie = MovieModel.objects.create(**validated_data)
        if genres:
            movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop("genres", None)
        # оновлюємо решту полів
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # оновлюємо M2M, якщо прийшло поле genres
        if genres is not None:
            instance.genres.set(genres)
        return instance


class MoviePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ('picture',)
        extra_kwargs = {'picture': {'required': True}}