from django.urls import path

from apps.tickets.views import TicketsDetailView, TicketsListView, ticket_qr_view

urlpatterns = [
    path("", TicketsListView.as_view(), name="ticket_list"),
    path("<int:pk>/", TicketsDetailView.as_view(), name="ticket_detail"),
    path("<int:pk>/qr/", ticket_qr_view, name="ticket_qr"),
]
