from django.urls import path

from apps.halls.views import HallDetailView, HallListCreateView, HallSeatDetailView, HallSeatListView

urlpatterns = [
    path('', HallListCreateView.as_view(), name='hall_list'),
    path('/<int:pk>', HallDetailView.as_view(), name='hall_detail'),

    path('/<int:hall_id>/seats', HallSeatListView.as_view(), name='hall_seats'),
    path('/seats/<int:pk>', HallSeatDetailView.as_view(), name='hall_seats'),
]