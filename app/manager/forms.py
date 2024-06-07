from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
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

class addSensorForm(ModelForm):
    class Meta:
        model = WaterReading
        fields = ['level', 'orp', 'ph', 'bod', 'temperature']
        widgets = {
            'level' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full', 'placeholder' : 'level', 'max' : '5'}
            ),
            'orp' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full'}
            ),
            'bod' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full'}
            ),
            'temperature' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full'}
            )
        }

    

    #level = forms.FloatField(
    #    max_value=1000,
    #    widget=forms.NumberInput(attrs={'class' : 'caret-pink-500 w-full'})
    #)