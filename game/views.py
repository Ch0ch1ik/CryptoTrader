from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import ScoreboardEntry
from .models import CryptoCurrency, Transaction
from .forms import BuyCurrencyForm, SellCurrencyForm


def home(request):
    currencies = CryptoCurrency.objects.all()
    scoreboard = ScoreboardEntry.objects.order_by('-score')[:10]
    context = {'currencies': currencies, 'scoreboard': scoreboard}
    return render(request, 'game/home.html', context)


def currency_list(request):
    currencies = CryptoCurrency.objects.all()
    return render(request, 'game/currency_list.html', {'currencies': currencies})


def currency_detail(request, pk):
    currency = get_object_or_404(CryptoCurrency, pk=pk)
    return render(request, 'game/currency_detail.html', {'currency': currency})


@login_required
def portfolio(request):
    transactions = Transaction.objects.filter(user=request.user)
    currencies = CryptoCurrency.objects.all()
    total_balance = request.user.profile.balance + sum([t.quantity * t.crypto_currency.price for t in transactions])
    context = {'transactions': transactions, 'currencies': currencies, 'total_balance': total_balance}
    return render(request, 'game/portfolio.html', context)


@login_required
def buy_currency(request, pk):
    currency = get_object_or_404(CryptoCurrency, pk=pk)
    if request.method == 'POST':
        form = BuyCurrencyForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if request.user.profile.balance >= quantity * currency.price:
                transaction = Transaction(currency=currency, user=request.user.profile, value=quantity * currency.price)
                transaction.save()
                request.user.profile.balance -= quantity * currency.price
                request.user.profile.save()
                messages.success(request, f'You have bought {quantity} {currency.name}!')
                return redirect('game:currency_list')
            else:
                messages.error(request, 'You do not have enough money to buy this currency!')
    else:
        form = BuyCurrencyForm()
    return render(request, 'game/buy_currency.html', {'form': form, 'currency': currency})


@login_required
def sell_currency(request, pk):
    currency = get_object_or_404(CryptoCurrency, pk=pk)
    if request.method == 'POST':
        form = SellCurrencyForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if request.user.profile.has_currency(currency, quantity):
                transaction = Transaction.objects.create(
                    user=request.user.profile,
                    crypto_currency=currency,
                    value=-quantity * currency.price,
                )
                request.user.profile.update_balance(quantity * currency.price)
                messages.success(request, f'You have sold {quantity} {currency.name} for {quantity * currency.price}.')
                return redirect('game:portfolio')
            else:
                messages.error(request, f'You do not have enough {currency.name}.')
    else:
        form = SellCurrencyForm()
    return render(request, 'game/sell_currency.html', {'form': form, 'currency': currency})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user.profile).order_by('-date')
    return render(request, 'game/transaction_history.html', {'transactions': transactions})
