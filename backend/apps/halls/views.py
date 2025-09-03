from django.shortcuts import render

from rest_framework import permissions, status
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
from rest_framework.response import Response

from apps.halls.models import HallModel, HallSeatModel
from apps.halls.serializer import HallSeatSerializer, HallSerializer


# Create your views here.
class HallListView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()




class HallDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()


# HallSeat


class HallSeatListView(ListCreateAPIView):
    serializer_class = HallSeatSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        hall_id = self.kwargs.get("hall_id")
        return HallSeatModel.objects.filter(hall_id=hall_id)

    def create(self, request, *args, **kwargs):
        hall_id = self.kwargs.get("hall_id")

        # перевіряємо, чи прийшов список, чи один об’єкт
        many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)

        # створюємо екземпляри
        seats = [
            HallSeatModel(hall_id=hall_id, **seat)
            for seat in serializer.validated_data
        ]
        HallSeatModel.objects.bulk_create(seats)

        return Response({"created": len(seats)}, status=status.HTTP_201_CREATED)

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


