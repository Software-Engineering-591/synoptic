from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from .models import WaterReading, Sensor

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

class addSensorForm(forms.Form):
    name = forms.CharField()
    uuid = forms.UUIDField()
    level = forms.FloatField()
    orp = forms.FloatField()  # oxidation reduction potential
    ph = forms.FloatField()
    bod = forms.FloatField()
    temperature = forms.FloatField # Celsius
