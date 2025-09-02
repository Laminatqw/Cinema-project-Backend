from django.db import models

from core.models import BaseModel


# Create your models here.
class HallModel(BaseModel):
    class Meta:
        db_table = 'halls'
    STANDARD = 'standard'
    IMAX = 'imax'
    THREE_D = '3d'

    HALL_TYPES = [
        (STANDARD, 'Standard'),
        (IMAX, 'IMAX'),
        (THREE_D, '3D'),
    ]

    title = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    hall_type = models.CharField(max_length=50, choices=HALL_TYPES, default=STANDARD)

class HallSeatModel(BaseModel):
    class Meta:
        db_table = 'hall_seats'
        unique_together = (('hall', 'row', 'number'),)

    SEAT_TYPES = [
        ("regular", "Regular"),
        ("vip", "VIP"),
        ("disabled", "Accessible"),
    ]

    hall = models.ForeignKey(HallModel, on_delete=models.CASCADE, related_name="seats")
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES, default="regular")

