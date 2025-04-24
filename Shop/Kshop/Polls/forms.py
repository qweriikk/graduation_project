from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_registration.forms import RegistrationForm
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки', 'rows': 3}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    
class CustomRegistrationForm(RegistrationForm):
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')