from django.urls import path

from apps.movies.views import (
    GenreDetailAPIView,
    GenresListCreateAPIView,
    MovieAddPhoto,
    MovieDetailView,
    MovieListCreateView,
)

urlpatterns = [
    path('', MovieListCreateView.as_view(), name='movie_list'),
    path('/<int:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('/<int:pk>/poster', MovieAddPhoto.as_view(), name='movie_poster'),
    path('/genres', GenresListCreateAPIView.as_view(), name='genres_list'),
    path('/genres/<int:pk>', GenreDetailAPIView.as_view(), name='genres_detail'),

]

