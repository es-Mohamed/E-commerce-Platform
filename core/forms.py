from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class Loginform(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Your Name",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "off"
        
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "current-password"
    }))


class Signupform(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Your Name",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "off"
        
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder": "Your Email",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "off"
        
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "new-password"
        
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Repeat Password",
        "class":"w-full py-4 px-6 rounded-xl",
        "autocomplete": "new-password"
        
    }))



