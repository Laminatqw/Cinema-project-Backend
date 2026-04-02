from django.shortcuts import render

from rest_framework import permissions, status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView, RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.halls.models import HallModel, HallSeatModel
from apps.halls.serializer import HallSeatSerializer, HallSerializer


# Create your views here.
class HallListCreateView(ListCreateAPIView):
    """
        get:
            shows all halls(for all users)
        post:
            creates a new hall(only for staff)
        """

    serializer_class = HallSerializer
    queryset = HallModel.objects.all()




    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class HallDetailView(RetrieveUpdateDestroyAPIView):
    """
        get:
            shows hall by id
        post:
            creates a new hall(only for staff)
        patch:
            updates a hall by id(only for staff)
        delete:
            deletes a hall by id(only for staff)
    """
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()





    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

# HallSeat


class HallSeatListCreateView(ListCreateAPIView):
    """
    get:
        shows all hall seats(for all users) by hall_id
    post
        creates a new hall seat|seats(only for staff) by hall_id
    """

    serializer_class = HallSeatSerializer
    pagination_class = None

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

    
class HallSeatDetailView(RetrieveDestroyAPIView):
    """
    get:
        shows seat by id(for all users)
    delete:
        deletes seat by id(only for staff) or all seats by hall_id if no pk
    """

    permission_classes = (IsAdminUser,)
    serializer_class = HallSeatSerializer
    queryset = HallSeatModel.objects.all()

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        hall_id = kwargs.get('hall_id')

        if pk:
            # видалення одного місця
            return super().delete(request, *args, **kwargs)
        elif hall_id:
            # видалення всіх місць залу
            deleted, _ = HallSeatModel.objects.filter(hall_id=hall_id).delete()
            return Response({"deleted": deleted}, status=status.HTTP_200_OK)

        return Response({"error": "No pk or hall_id provided"}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class HallSeatUpdateView(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSeatSerializer
    def put(self, request, *args, **kwargs):
        hall_id = self.kwargs.get("hall_id")

        many = isinstance(request.data, list)
        if not many:
            return Response({"error": "Expected a list"}, status=status.HTTP_400_BAD_REQUEST)

        updated = []
        for seat_data in request.data:
            seat_id = seat_data.get("id")
            if not seat_id:
                continue
            try:
                seat = HallSeatModel.objects.get(id=seat_id, hall_id=hall_id)
                serializer = self.get_serializer(seat, data=seat_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated.append(serializer.data)
            except HallSeatModel.DoesNotExist:
                continue

        return Response({"updated": len(updated)}, status=status.HTTP_200_OK)



