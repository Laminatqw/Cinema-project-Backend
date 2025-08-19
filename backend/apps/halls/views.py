from django.shortcuts import render

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.halls.models import HallModel
from apps.halls.serializer import HallSerializer


# Create your views here.
class HallListView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(storage_id=1)
        super().perform_create(serializer)


class HallDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HallSerializer
    queryset = HallModel.objects.all()






