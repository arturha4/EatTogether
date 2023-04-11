from django.db import models
from users.models import CustomUser


class Cooperation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(CustomUser, related_name='joined_events')
