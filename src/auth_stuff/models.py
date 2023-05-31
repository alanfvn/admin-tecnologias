from django.db import models
from dashboard.models import Region

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
