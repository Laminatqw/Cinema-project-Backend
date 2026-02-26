import uuid

from django.db import models

from core.models import BaseModel

from apps.halls.models import HallSeatModel
from apps.sessions.models import SessionModel
from apps.users.models import UserModel

# Create your models here.

class TicketModel(BaseModel):
    class Meta:
        db_table = 'tickets'
        unique_together = ("session", "seat")
    STATUS_CHOICES = [
        ("reserved", "Reserved"),  # заброньований, але ще не оплачений
        ("paid", "Paid"),  # оплачений
        ("canceled", "Canceled"),  # відмінений
        ("used","Used"),# використаний
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    seat = models.ForeignKey(HallSeatModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reserved")
    # qr_code = models.ImageField(upload_to="photo_storage/qr_codes/", blank=True, null=True)

    read_only_fields = ["status", "created_at"]


