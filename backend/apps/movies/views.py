from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions.is_superuser_permission import IsSuperUser

from apps.movies.models import MovieModel
from apps.movies.serializer import MovieSerializer

# Create your views here.

class MovieListView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()

class MovieCreateView(CreateAPIView):
    serializer_class = MovieSerializer
    queryset = MovieModel.objects.all()
    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        print("AUTH HEADER:", request.headers.get("Authorization"))
        print("USER:", request.user)
        print("IS STAFF:", request.user.is_staff)
        print("IS SUPERUSER:", request.user.is_superuser)
        return super().post(request, *args, **kwargs)

class MovieDetailView(RetrieveUpdateDestroyAPIView):
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


