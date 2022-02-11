from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_distributor = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)
    is_telecaller = models.BooleanField(default=False)
