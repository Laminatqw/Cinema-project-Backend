from django.db import models

from core.models import BaseModel


# Create your models here.
class HallModel(BaseModel):
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


