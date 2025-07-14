from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from apps.movies.models import MovieModel
from apps.movies.serializer import MovieSerializer

# Create your views here.

class MovieListView(ListAPIView):
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieDetailView(RetrieveAPIView):
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieCreateView(CreateAPIView):
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()



