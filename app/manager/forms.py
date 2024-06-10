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
                attrs = {'class' : 'w-full h-full', 'placeholder' : 'orp'}
            ),
            'bod' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full', 'placeholder' : 'bod'}
            ),
            'temperature' : forms.NumberInput(
                attrs = {'class' : 'w-full h-full', 'placeholder' : 'temperature'}
            ),
            'ph' : forms.NumberInput(
                attrs= {'class' : 'w-full h-full', 'placeholder' : 'pH', 'max' : '14'}
            )
        }
class latandlon(forms.Form):
    lat = forms.FloatField(
        widget = forms.NumberInput(attrs={'id' : 'lat'})
    )
    lon = forms.FloatField(
        widget = forms.NumberInput(attrs={'id' : 'lon'})
    )
