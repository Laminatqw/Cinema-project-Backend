from django.urls import path

from apps.tickets.views import TicketQRView, TicketsDetailView, TicketsListView, TicketValidateView

urlpatterns = [
    path("", TicketsListView.as_view(), name="ticket_list"),
    path("/<int:pk>", TicketsDetailView.as_view(), name="ticket_detail"),
    path("/<int:pk>/qr", TicketQRView.as_view(), name="ticket_qr"),
    path("/validate", TicketValidateView.as_view(), name="ticket_validate"),
]
