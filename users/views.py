from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse

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


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()
            return redirect('users:thanks_user')  # Перенаправляем на страницу успешной регистрации
    else:
        form = RegisterUserForm()  # Пустая форма для GET-запроса
    return render(request, 'users/register.html', {'form': form})


def thanks(request):
    return render(request, 'users/thanks.html')