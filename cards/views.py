from django.http import HttpResponse
from django.shortcuts import render


def catalog(request):
    return HttpResponse("Каталог карточек")


def get_card_by_id(request, card_id):
    return HttpResponse(f"Карточка {card_id}")


def get_category_by_name(request, slug):
    return HttpResponse(f"Категория {slug}")
