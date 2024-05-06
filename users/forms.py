from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterUserForm(UserCreationForm):
    pass

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))