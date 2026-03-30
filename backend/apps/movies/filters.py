from django.utils.timezone import now

from django_filters import rest_framework as filters

from apps.movies.models import MovieModel


class MovieFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    genre = filters.BaseInFilter(field_name="genres__id", lookup_expr="in")
    is_now_showing = filters.ChoiceFilter(
        choices=(('yes', 'Yes'), ('no', 'No')),
        method='filter_is_now_showing',
        label='Is Now Showing'
    )
    rating__gte = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    rating__lte = filters.NumberFilter(field_name="rating", lookup_expr="lte")
    length__gte = filters.NumberFilter(field_name="length", lookup_expr="gte")
    length__lte = filters.NumberFilter(field_name="length", lookup_expr="lte")
    year__exact = filters.NumberFilter(field_name="year", lookup_expr="exact")
    year__gte = filters.NumberFilter(field_name="year", lookup_expr="gte")
    year__lte = filters.NumberFilter(field_name="year", lookup_expr="lte")

    class Meta:
        model = MovieModel
        fields = ['name', 'genres', 'rating__gte', 'rating__lte',
                  'length__gte', 'length__lte', 'year__exact',
                  'year__gte', 'year__lte', 'is_now_showing']

    def filter_is_now_showing(self, queryset, name, value):
        today = now().date()
        if value == 'yes':
            return queryset.filter(release_date__lte=today, end_date__gte=today)
        elif value == 'no':
            return queryset.exclude(release_date__lte=today, end_date__gte=today)
        return queryset