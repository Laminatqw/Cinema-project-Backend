from django.urls import path

from .views import SessionDetailView, SessionListView

urlpatterns = [
    path("", SessionListView.as_view(), name="session_list_create"),
    path("/<int:pk>", SessionDetailView.as_view(), name="session_detail"),
]