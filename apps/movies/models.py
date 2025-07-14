from django.db import models

from core.models import BaseModel

# Create your models here.

class MovieModel(BaseModel):
    class Meta:
        db_table = 'movies'
    name = models.CharField(max_length=100)
    length = models.IntegerField()
    picture = models.ImageField(upload_to='movies/')
    trailer_link = models.URLField()
    rating = models.IntegerField()
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    is_now_showing = models.BooleanField()

