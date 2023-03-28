from django.contrib.auth.models import User
from django.db import models

from game.models import Transaction


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def has_currency(self, currency, quantity):
        try:
            transaction = Transaction.objects.filter(user=self.user, crypto_currency=currency).order_by('-date')[0]
        except IndexError:
            return False
        if transaction.quantity >= quantity:
            return True
        else:
            return False

    def update_balance(self, amount):
        self.balance += amount
        self.save()


class ScoreboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return f'{self.user.username} - Score: {self.score}'
