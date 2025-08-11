from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.movies.models import MovieModel
from apps.movies.serializer import MovieSerializer

# Create your views here.

class MovieListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieCreateView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieAddPhoto(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()
    http_method_names = ['patch']

    def perform_update(self, serializer):
        movie = self.get_object()
        movie.picture.delete()
        super().perform_update(serializer)


