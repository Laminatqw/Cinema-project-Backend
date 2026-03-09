from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from apps.movies.filters import MovieFilter
from core.permissions.is_superuser_permission import IsSuperUser

# from urllib3 import request

from apps.movies.models import GenreModel, MovieModel
from apps.movies.serializer import GenreSerializer, MovieSerializer

# Create your views here.

class MovieListCreateView(ListCreateAPIView):

    """
    get:
        shows all movies(for anyone)
    post:
        creates a new movie(for staff only)
    """

    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter


    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]



class MovieDetailView(RetrieveUpdateDestroyAPIView):

    """
    get:
        shows one movie by id(for anyone)
    patch:
        edits movie info by id(for staff)
    destroy:
        deletes movie by id(for staff)
    """

    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]



class MovieAddPhoto(UpdateAPIView):
    """
    patch:
        adds photo|poster to movie by id(for staff)
    """
    permission_classes = (IsAdminUser,)
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()
    http_method_names = ['patch']

    def perform_update(self, serializer):
        movie = self.get_object()
        movie.picture.delete()
        super().perform_update(serializer)

class GenresListCreateAPIView(ListCreateAPIView):
    """
    get:
        shows all genres(for anyone)
    post:
        creates genre(for staff only)
    """
    serializer_class = GenreSerializer
    queryset = GenreModel.objects.all()
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):

    """
    get:
        shows one genre by id(for anyone)
    patch:
        edits genre info by id(for staff)
    delete:
        deletes genre by id(for staff)
    """

    serializer_class = GenreSerializer
    queryset = GenreModel.objects.all()



    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
