from django.utils.timezone import now

from django_filters import rest_framework as filters

from apps.movies.models import MovieModel


class MovieFilter(filters.FilterSet):

    name = filters.CharFilter(lookup_expr="icontains")
    genre = filters.BaseInFilter(field_name="genre__id", lookup_expr="in")

    class Meta:
        model = MovieModel
        fields = {
            "rating": ["exact", "gte", "lte"],
            "length": ["gte", "lte"],
            "year": ["exact", "gte", "lte"],
            }

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
        fields = ['name','genre', 'rating','length','year','is_now_showing']

    def filter_is_now_showing(self, queryset, name, value):
        today = now().date()
        if value == 'yes':
            return queryset.filter(release_date__lte=today, end_date__gte=today)
        elif value == 'no':
            return queryset.exclude(release_date__lte=today, end_date__gte=today)
        return queryset