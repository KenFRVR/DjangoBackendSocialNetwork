from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    participants = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(default='logo.svg')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text
