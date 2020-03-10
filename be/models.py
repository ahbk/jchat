from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
