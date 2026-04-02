from django_filters import rest_framework as filters
from apps.sessions.models import SessionModel

class SessionFilter(filters.FilterSet):
    movie = filters.BaseInFilter(field_name="movie__id", lookup_expr="in")
    date = filters.DateFilter(field_name="start_time", lookup_expr="date")
    hall_type = filters.CharFilter(field_name="hall__hall_type", lookup_expr="exact")
    movie_name = filters.CharFilter(field_name="movie__name", lookup_expr="icontains")

    class Meta:
        model = SessionModel
        fields = ['movie', 'date', 'hall_type', 'movie_name']