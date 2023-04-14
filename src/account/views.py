from django.shortcuts import render, redirect
from account.forms import AccountAuthenticationForm, loginForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from .models import Account


def authenticate_view(request):
    context = {}

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            phone_number = request.POST['phone_number']
            if Account.objects.filter(phone_number=phone_number).exists():
                id = Account.objects.filter(phone_number=phone_number).values_list('id', flat=True)
                for anyID in id:
                    return redirect(f"login/{anyID}/")
            else:
                return redirect(f"register/{phone_number}/")

    else: # Get request
        form = AccountAuthenticationForm()

    context['authenticate_form'] = form

    return render(request, 'account/authenticate.html', context)


def login_view(request, account_id):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    phone_number_query = Account.objects.filter(id=account_id).values_list('phone_number', flat=True)
    for anyPhone in phone_number_query:
                phone = anyPhone
    context['phone_number'] = phone

    if request.POST:
        form = loginForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            user = authenticate(phone_number=phone, password= password)

            if user:
                login(request, user)
                return redirect("home")

    else: # Get request
        form = loginForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def register_view(request, phone_number):
    context = {}

    # if request.POST:
    #      form = RegistrationForm(request.POST)
    #      if form.is_valid():
    #           form.save()


    return render(request, 'account/register.html', {})