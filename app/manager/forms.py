from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm


class login_form(AuthenticationForm):
    ## Fields for login form, seems for username, to enforce clientside, need a camal cased maxLength html attribute to enforce
    username = forms.CharField(
        max_length = 50,
        widget=forms.TextInput(attrs={'class': 'w-full caret-pink-500', 'placeholder' : 'username', 'maxLength' : '50'})
    )
    password = forms.CharField(
        max_length= 50,
        widget=forms.PasswordInput(attrs={'class': 'caret-pink-500 w-full', 'placeholder' : 'password'})
    )

    class Meta:
        fields = ('username', 'password')
