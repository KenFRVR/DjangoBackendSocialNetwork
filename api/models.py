from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Jhon Doe")
    bio = models.TextField(blank=True, default='This is my bio')

    def __str__(self):
        return self.name
