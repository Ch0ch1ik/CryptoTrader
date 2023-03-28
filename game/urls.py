from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('currencies/', views.currency_list, name='currency_list'),
    path('currencies/<int:pk>/', views.currency_detail, name='currency_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('buy/<int:pk>/', views.buy_currency, name='buy_currency'),
    path('sell/<int:pk>/', views.sell_currency, name='sell_currency'),
    path('transactions/', views.transaction_history, name='transaction_history'),
]
