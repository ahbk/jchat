from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
