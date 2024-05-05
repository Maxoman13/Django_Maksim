from django.shortcuts import render
from django.http import HttpResponse


def login_user(request):
    # Здесь будет реализация входа
    return HttpResponse("Вы вошли в систему")


def logout_user(request):
    # Здесь будет реализация выхода
    return HttpResponse("Вы вышли из системы")


def signup_user(request):
    pass


def thanks_user(request):
    pass
