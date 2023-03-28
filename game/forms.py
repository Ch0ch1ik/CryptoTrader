from django import forms
from .models import Transaction


class BuyCurrencyForm(forms.Form):
    quantity = forms.DecimalField(label='Quantity', max_digits=20, decimal_places=10)


class SellCurrencyForm(forms.Form):
    quantity = forms.DecimalField(label='Quantity', max_digits=20, decimal_places=10)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['currency', 'quantity']
