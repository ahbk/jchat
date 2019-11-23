from django.db import models

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255, unique=True)
    confirmed = models.DateTimeField(null=True)

class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sign = models.CharField(max_length=16, unique=True)

class Member(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sign = models.CharField(max_length=16)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notifications = models.BooleanField(default=False)

    class Meta:
        unique_together = [['group', 'sign']]

class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    parents = models.ManyToManyField('Message')
