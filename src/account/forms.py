from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
# my models
from account.models import Account, OtpCode
 
# UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="ایمیل خود را وارد کنید")

    class Meta:
        model = Account
        fields = ["phone_number", "email", "first_name", "last_name", "password1", "password2",]

        def clean(self) :
            phone_number            = self.cleaned_data['phone_number']
            email                   = self.cleaned_data['email']
            first_name              = self.cleaned_data['first_name']
            last_name               = self.cleaned_data['last_name']
            password1               = self.cleaned_data['password1']
            password2               = self.cleaned_data['password2']
        

class AccountAuthenticationForm(forms.ModelForm):

    phone_number = forms.CharField(label="شماره موبایل", max_length=11)

    class Meta:
        model = Account
        fields = ['phone_number']

    def clean(self) :
        phone_number = self.cleaned_data['phone_number']


class loginForm(forms.ModelForm):

    password = forms.CharField(label='پسورد', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['password',]

    def clean(self) :
        password = self.cleaned_data['password']

        # if not authenticate(password = password):
        #     raise forms.ValidationError("Invalid login")


class OtpFormPhoneNumber(forms.ModelForm):

    class Meta:
        model = OtpCode
        fields = ['otp']


class OtpForm(forms.ModelForm):

    otp = forms.IntegerField()

    class Meta:
        model = OtpCode
        fields = ['otp',]

    def clean(self) :
        otp = self.cleaned_data['otp']