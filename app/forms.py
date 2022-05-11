from dataclasses import fields
from enum import unique
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer



class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField( label='Email',widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username' : forms.TextInput(attrs={'class' : 'form-control'})}


class Login(AuthenticationForm):
    username = UsernameField(widget= forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField( label = _('Password'), widget= forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}))

class changepassword(PasswordChangeForm):
    old_password = forms.CharField(label= _('Old Password'), widget=forms.PasswordInput(attrs={'autocomplete': 'current-password' ,'autofocus': True, 'class': 'form-control'}))
    new_password = forms.CharField(label= _('New Password'), widget=forms.PasswordInput(attrs={'autocomplete': 'new-password' ,'autofocus': True, 'class': 'form-control'}) ,help_text= password_validation.password_validators_help_text_html())
    confirm_password = forms.CharField(label= _('Confirm Password'), widget=forms.PasswordInput(attrs={'autocomplete': 'new-password' ,'autofocus': True, 'class': 'form-control'}))

class profile(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'zipcode', 'state']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'locality': forms.TextInput(attrs={'class': 'form-control'}), 'state': forms.Select(attrs={'class': 'form-control'}), 'city': forms.TextInput(attrs={'class': 'form-control'}), 'zipcode': forms.NumberInput(attrs={'class': 'form-control'}), }



    