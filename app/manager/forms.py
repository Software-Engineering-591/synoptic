from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import WaterReading, Sensor
from django.utils.translation import gettext_lazy as _


class Loginform(AuthenticationForm):
    ## Fields for login form, seems for username, to enforce clientside
    # , need a camal cased maxLength html attribute to enforce
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'w-full caret-pink-500',
                'placeholder': 'username',
                'maxLength': '50',
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={'class': 'caret-pink-500 w-full', 'placeholder': 'password'}
        ),
    )

    class Meta:
        fields = ('username', 'password')


class Addwaterform(ModelForm):
    class Meta:
        model = WaterReading
        fields = ['level', 'orp', 'ph', 'bod', 'temperature']
        widgets = {
            'level': forms.NumberInput(
                attrs={
                    'class': 'w-full h-full',
                    'placeholder': _('level-for-sensor-individual'),
                }
            ),
            'orp': forms.NumberInput(
                attrs={
                    'class': 'w-full h-full',
                    'placeholder': _('Oxidation-Reduction Potential'),
                }
            ),
            'bod': forms.NumberInput(
                attrs={
                    'class': 'w-full h-full',
                    'placeholder': _('Biochemical-oxygen-demand'),
                }
            ),
            'temperature': forms.NumberInput(
                attrs={
                    'class': 'w-full h-full',
                    'placeholder': _('temperature-for-sensor-individual'),
                }
            ),
            'ph': forms.NumberInput(
                attrs={'class': 'w-full h-full', 'placeholder': 'pH', 'max': '14'}
            ),
        }


class Latandlon(forms.Form):
    lat = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'id': 'lat'}
        )
    )
    lon = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'lon'}))


class Addsensorform(ModelForm):
    class Meta:
        model = Sensor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'w-full h-full',
                    'placeholder': _('sensor-name-individual'),
                    'id': 'name',
                },
            )
        }
        error_messages = {
            'name' :{
            'unique' : _('sensor-already-exists')
            }
        }
