from django.db import models
from users.models import CustomUser


class Cooperation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    creator = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(CustomUser, related_name='joined_events')

    def __str__(self):
        return self.title


class ProductExpiredNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
