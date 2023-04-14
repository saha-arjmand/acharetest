from django.shortcuts import render
from account.models import Account

def home_screen_view(request):

    context = {}

    # we need this queryset to show the accounts to achare team
    accounts = Account.objects.all()
    context['accounts'] = accounts

    return render(request, "home/home.html", context)
