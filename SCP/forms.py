from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from User.models import Customer

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'username', 'password1', 'password2']

