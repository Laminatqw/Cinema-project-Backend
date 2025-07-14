from rest_framework import serializers

from apps.movies.models import MovieModel


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ('name', 'length', 'picture', 'trailer_link', 'rating', 'genre', 'year', 'is_now_showing')