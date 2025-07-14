from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from core.models import BaseModel


class UserModel(AbstractBaseUser, BaseModel):

    class Meta:
        db_table = 'auth_user'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'


class Profile(BaseModel):
    class Meta:
        db_table = 'profile'
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)




# Create your models here.
