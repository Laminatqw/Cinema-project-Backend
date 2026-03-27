from django_filters import rest_framework as filters

from apps.sessions.models import SessionModel


class SessionFilter(filters.FilterSet):
    movie = filters.BaseInFilter(field_name="movie__id", lookup_expr="in")

    class Meta:
        model = SessionModel
        fields = ['movie',]