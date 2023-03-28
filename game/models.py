from django.db import models
from django.contrib.auth.models import User


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return f'{self.name} ({self.symbol})'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.currency.name}: {self.quantity}'
