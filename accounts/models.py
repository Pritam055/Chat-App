from django.db import models
  
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): 
    activated = models.BooleanField(default=False)
    token = models.CharField(max_length=250, null=True, blank=True)