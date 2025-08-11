from django_filters import rest_framework as filters

from apps.movies.models import MovieModel


class MovieFilter(filters.FilterSet):
    # rating = filters.NumberFilter(field_name='rating', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    length_max = filters.CharFilter(field_name='length', lookup_expr='gte')
    length_min = filters.CharFilter(field_name='length', lookup_expr='lte')
    rating = filters.CharFilter(field_name='rating', lookup_expr='exact')
    rating_max = filters.CharFilter(field_name='rating', lookup_expr='gte')
    rating_min = filters.CharFilter(field_name='rating', lookup_expr='lte')
    genre = filters.CharFilter(field_name='genre', lookup_expr='icontains')

    class Meta:
        model = MovieModel
        fields = ['name', 'length_max', 'length_min', 'rating_max', 'rating_min', 'genre', 'year_max', 'year_min', 'is_now_showing']