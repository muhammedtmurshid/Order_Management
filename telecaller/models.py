from django.db import models

# Create your models here.
from core.models import User


class TeleCaller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    mobile = models.CharField(max_length=12, default='+91')
    created_date= models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
