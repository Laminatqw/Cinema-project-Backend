from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.halls.models import HallModel, HallSeatModel
from apps.halls.serializer import HallSeatSerializer, HallSerializer


# Create your views here.
class HallListView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()




class HallDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()


# HallSeat


class HallSeatListView(ListCreateAPIView):
    serializer_class = HallSeatSerializer

    def get_queryset(self):
        hall_id = self.kwargs.get("hall_id")
        return HallSeatModel.objects.filter(hall_id=hall_id)

    def perform_create(self, serializer):
        hall_id = self.kwargs.get("hall_id")
        serializer.save(hall_id=hall_id)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
class HallSeatDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSeatSerializer
    queryset = HallSeatModel.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


