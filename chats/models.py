from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length = 50, unique=True)

    def get_absolute_url(self): 
        return reverse('group_chat', kwargs={'group_name': self.name})

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Group, self).save(*args, **kwargs)

class Chat(models.Model):
    content = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE )

