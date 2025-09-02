from django.db import models

from core.models import BaseModel

from apps.halls.models import HallModel
from apps.movies.models import MovieModel


# Create your models here.
class SessionModel(BaseModel):
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="sessions", blank=True, null=True)
    hall = models.ForeignKey(HallModel, on_delete=models.CASCADE, related_name="sessions", null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    price  = models.DecimalField(max_digits=8, decimal_places=2, default=0)
