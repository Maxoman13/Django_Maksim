from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from cards.views import MenuMixin
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(MenuMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm  # Указываем класс формы, который мы создали для регистрации
    template_name = 'users/register.html'  # Путь к шаблону, который будет использоваться для отображения формы
    extra_context = {'title': 'Регистрация'}  # Дополнительный контекст для передачи в шаблон
    success_url = reverse_lazy('users:thanks_user')  # URL, на который будет перенаправлен пользователь после успешной регистрации


def thanks(request):
    return render(request, 'users/thanks.html')