from django.urls import path

from apps.movies.views import MovieAddPhoto, MovieCreateView, MovieDetailView, MovieListView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('/create', MovieCreateView.as_view(), name='movie_create'),
    path('/<int:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('/<int:pk>/poster', MovieAddPhoto.as_view(), name='movie_poster'),

]