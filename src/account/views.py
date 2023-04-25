from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from account.forms import AccountAuthenticationForm, loginForm, RegistrationForm, OtpForm, OtpFormPhoneNumber
from django.contrib.auth import login, authenticate, logout
from .models import Account, OtpCode
from . import helper 
from django.http import HttpResponseRedirect
from django.urls import reverse

# Security Methods
from account.security_methods.wait_sms import wait_sms
from account.security_methods.otp_expiration import check_otp_expiration


def authenticate_view(request):
    context = {}

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            phone_number = request.POST['phone_number']

            # Check PhoneNumber and Email are xist
            account_exist = Account.objects.filter(phone_number=phone_number).exists()
            email_exist_query = Account.objects.filter(phone_number=phone_number).values_list('email', flat=True)
            for anyEmail in email_exist_query:
                if len(str(anyEmail)) > 0:
                    email_exist = True
                else:
                    email_exist = False

            # if account exist then login
            if  account_exist == True and email_exist == True:
                id = Account.objects.filter(phone_number=phone_number).values_list('id', flat=True)
                for anyID in id:
                    return redirect(f"login/{anyID}/")
            
            # phone number and email don't exist in database
            # if account does not exist then register
            else: 
                if wait_sms(phone_number): # Avoid repeated user requests    

                    if account_exist == False:
                        user = form.save(commit=False)
                        user.save()

                    # find id of user for create otp code
                    phone_number = request.POST['phone_number']
                    id = Account.objects.get(phone_number = phone_number)

                    # send otp
                    otp = helper.get_random_otp()
                    print(f"Otp for test is : {otp}")

                    # save otp data
                    otp_user = OtpCode(account= id, otp = otp)
                    otp_user.save()

                    return redirect(f"otp/{id.id}/")
                    # return redirect('home')
            
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


def otp_view(request, id):
    context = {}
    user = OtpCode.objects.get(account = id)


    if request.POST:
        form = OtpForm(request.POST)
        if form.is_valid():

            # check otp expiration
            if check_otp_expiration(id) == False :
                return HttpResponseRedirect(reverse('authenticate'))
            else:
                # Check otp is correct
                if user.otp != int(request.POST.get('otp')):
                    return HttpResponseRedirect(reverse('authenticate'))
                else:
                    # active user if otp correct
                    account = Account.objects.get(id = id)
                    account.is_active = True
                    account.save()
                    request.session['id'] = id
                    return redirect('register')
            
    else: # Get request
        form = OtpForm()



            # check user block
            # print(helper.block_wrong_password_check(phone_number))

                # block user

    context['otp_form'] = form
    return render(request, 'account/otp.html', context)


def register_view(request):
    context = {}

    # get id from session
    id = request.session.get('id')

    # get object that we want work on it
    obj = Account.objects.get(id = id)
    phone_number = obj.phone_number
    # for show phone number in the form
    context['phone_number'] = phone_number

    # becuase already we have form so we should update it
    form = RegistrationForm(instance = obj)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            
            # login
            phone = phone_number
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(phone_number= phone, password = raw_password)
            login(request, account)

            return redirect('home')
        else:
            print(form.errors.as_data()) # here you print errors to terminal

    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


