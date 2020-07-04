from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    userName = models.CharField(max_length = 35,unique=True)
    
    is_staff = models.BooleanField(('staff status'),default=False)
    is_superuser = models.BooleanField(('superuser status'),default=False)
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'userName'

    objects = CustomUserManager()
    
    def __str__(self):
        return self.userName


class highScores(models.Model):
    userName = models.CharField(primary_key=True,max_length = 20)
    time = models.FloatField()

class userData(models.Model):
    userName = models.CharField(max_length = 20)
    prevTime = models.CharField(max_length = 10)
    numberTries = models.CharField(max_length = 10)
    averageTime = models.CharField(max_length = 10)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)