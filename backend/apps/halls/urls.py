from django.urls import path

from apps.halls.views import HallDetailView, HallListView

urlpatterns = [
    path('', HallListView.as_view(), name='hall_list'),
    path('<int:pk>/', HallDetailView.as_view(), name='hall_detail'),
]