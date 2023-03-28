from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class ScoreboardEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.points}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=10, default=0)

    def __str__(self):
        return self.user.username
