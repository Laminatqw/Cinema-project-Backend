from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import BaseModel

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, BaseModel, PermissionsMixin):

    class Meta:
        db_table = 'auth_user'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True)
    age = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')



# Create your models here.
