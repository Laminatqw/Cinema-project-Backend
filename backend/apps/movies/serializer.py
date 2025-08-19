from rest_framework import serializers

from apps.movies.models import MovieModel


class MovieSerializer(serializers.ModelSerializer):

    is_now_showing = serializers.SerializerMethodField()

    class Meta:
        model = MovieModel
        fields = ('name', 'length', 'picture', 'trailer_link', 'rating', 'genre', 'year', 'is_now_showing')

    def get_is_now_showing(self, obj):
        return obj.is_now_showing

class MoviePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ('picture',)
        extra_kwargs = {'picture': {'required': True}}