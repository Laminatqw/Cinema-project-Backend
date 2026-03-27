from django.urls import path

from .views import SessionDetailView, SessionListView, SessionPriceListView, SessionPriceDetailView, SessionSeatsView

urlpatterns = [
    path("", SessionListView.as_view(), name="session_list_create"),
    path("/<int:pk>", SessionDetailView.as_view(), name="session_detail"),
    path("/<int:session_id>/prices", SessionPriceListView.as_view(), name="session_prices"),
    path("/<int:session_id>/prices/<int:pk>", SessionPriceDetailView.as_view(), name="session_price_detail"),
    path("/<int:session_id>/seats", SessionSeatsView.as_view(), name="session_seats"),
]