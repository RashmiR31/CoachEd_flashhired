from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='IN')
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2','phone_number','is_candidate','is_recruiter')

