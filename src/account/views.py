from django.shortcuts import render, redirect
from account.forms import AccountAuthenticationForm, loginForm, RegistrationForm, OtpForm, OtpFormPhoneNumber
from django.contrib.auth import login, authenticate, logout
from .models import Account, OtpCode
from . import helper 
from django.http import HttpResponseRedirect
from django.urls import reverse


def authenticate_view(request):
    context = {}

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            phone_number = request.POST['phone_number']

            account_exist = Account.objects.filter(phone_number=phone_number).exists()
            email_exist_query = Account.objects.filter(phone_number=phone_number).values_list('email', flat=True)
            for anyEmail in email_exist_query:
                if len(str(anyEmail)) > 0:
                    email_exist = True
                else:
                    email_exist = False

            if  account_exist == True and email_exist == True:
                id = Account.objects.filter(phone_number=phone_number).values_list('id', flat=True)
                for anyID in id:
                    return redirect(f"login/{anyID}/")
            
            else: # phone number does not exist in database
                form = OtpFormPhoneNumber(request.POST)
                account_exist = OtpCode.objects.filter(phone_number=phone_number).exists()
                if form.is_valid():
                    if account_exist == False:
                        user = form.save(commit=False)
                        # send otp
                        otp = helper.get_random_otp()
                        print(f"Otp for test is : {otp}")
                        # helper.sent_otp(phone_number, otp)
                        # save otp
                        user.otp = otp
                        user.save()
                        return redirect(f"otp/{phone_number}/")
                    else:
                        # send otp
                        otp = helper.get_random_otp()
                        print(f"Otp for test is : {otp}")
                        # helper.sent_otp(phone_number, otp)
                        user = OtpCode.objects.filter(phone_number=phone_number).update(otp=otp)
                        return redirect(f"otp/{phone_number}/")
                    

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


def otp_view(request, phone_number):
    context = {}

    user = OtpCode.objects.get(phone_number = phone_number)

    if request.POST:
        form = OtpForm(request.POST)
        if form.is_valid():
            if user.otp != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('authenticate'))
            else:
                user.is_active = True
                user.save()
                try:
                    request.session['user_mobile'] = phone_number
                    return redirect('register')
                except Exception as e:
                    print(e)

    else: # Get request
        form = OtpForm()


    context['otp_form'] = form
    return render(request, 'account/otp.html', context)


def register_view(request):
    phone_number = request.session.get('user_mobile')
    context = {}
    context['phone_number'] = phone_number

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone = phone_number
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(phone_number= phone, password = raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


