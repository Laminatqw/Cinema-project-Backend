from django.db import models
from django.utils import timezone

from core.models import BaseModel

from apps.halls.models import HallModel, HallSeatModel
from apps.movies.models import MovieModel


# Create your models here.
class SessionModel(BaseModel):
    class Meta:
        db_table = 'sessions'

    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="sessions", blank=True, null=True)
    hall = models.ForeignKey(HallModel, on_delete=models.CASCADE, related_name="sessions", null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if self.end_time < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

class SessionPriceModel(BaseModel):
    class Meta:
        db_table = 'session_prices'
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name="prices", blank=True, null=True)
    seat_type = models.CharField(max_length=20, choices=HallSeatModel.SEAT_TYPES, default= 'regular')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
