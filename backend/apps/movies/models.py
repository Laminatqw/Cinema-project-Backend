from django.db import models
from django.utils.timezone import now

from core.models import BaseModel

from apps.movies.services import upload_poster

# Create your models here.

class MovieModel(BaseModel):
    class Meta:
        db_table = 'movies'
    name = models.CharField(max_length=100)
    length = models.IntegerField()
    picture = models.ImageField(upload_to=upload_poster, blank=True)
    trailer_link = models.URLField()
    rating = models.IntegerField()
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def is_now_showing(self):
        today = now().date()
        return self.release_date <= today <= self.end_date


