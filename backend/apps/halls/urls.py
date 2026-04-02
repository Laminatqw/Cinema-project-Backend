from django.urls import path

from apps.halls.views import HallDetailView, HallListCreateView, HallSeatDetailView, HallSeatListCreateView, \
    HallSeatUpdateView

urlpatterns = [
    path('', HallListCreateView.as_view(), name='hall_list'),
    path('/<int:pk>', HallDetailView.as_view(), name='hall_detail'),

    path('/<int:hall_id>/seats', HallSeatListCreateView.as_view(), name='hall_seats'),
    path('/seats/<int:pk>', HallSeatDetailView.as_view(), name='hall_seats'),
    path("/<int:hall_id>/seats/delete-all", HallSeatDetailView.as_view(), name="hall_seats_bulk_delete"),

    path('/<int:hall_id>/seats/update', HallSeatUpdateView.as_view(), name='hall_seats'),
]