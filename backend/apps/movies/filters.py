from django.utils.timezone import now

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
    year = filters.CharFilter(field_name='year', lookup_expr='year')
    year_max = filters.CharFilter(field_name='year', lookup_expr='year__gte')
    year_min = filters.CharFilter(field_name='year', lookup_expr='year__lte')

    IS_NOW_SHOWING_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    is_now_showing = filters.ChoiceFilter(
        choices=IS_NOW_SHOWING_CHOICES,
        method='filter_is_now_showing',
        label='Is Now Showing'
    )

    class Meta:
        model = MovieModel
        fields = ['name', 'length_max', 'length_min', 'rating_max', 'rating_min', 'genre', 'year_max', 'year_min', 'is_now_showing']

    def filter_is_now_showing(self, queryset, name, value):
        today = now().date()
        if value == 'yes':
            return queryset.filter(release_date__lte=today, end_date__gte=today)
        elif value == 'no':
            return queryset.exclude(release_date__lte=today, end_date__gte=today)
        return queryset