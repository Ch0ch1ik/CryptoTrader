from django import forms
from .models import CryptoCurrency


class BuyCurrencyForm(forms.Form):
    currency = forms.CharField(max_length=50)
    user = forms.CharField(max_length=50)
    quantity = forms.IntegerField(min_value=1)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity * self.currency.price > self.user.profile.balance:
            raise forms.ValidationError('You do not have enough money to buy this currency!')
        return quantity


class SellCurrencyForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.currency = kwargs.pop('currency')
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if not self.user.profile.has_currency(self.currency, quantity):
            raise forms.ValidationError(f'You do not have enough {self.currency.name}.')
        return quantity


class AddCurrencyForm(forms.ModelForm):
    class Meta:
        model = CryptoCurrency
        fields = ['name', 'symbol', 'value', 'price']
