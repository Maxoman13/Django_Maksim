from django.http import HttpResponse
from django.shortcuts import render
from .models import Card

cards_dataset = [
    {"question": "Что такое PEP 8?",
     "answer": "PEP 8 — стандарт написания кода на Python.",
     "category": "Стандарты кода",
     "tags": ["PEP 8", "стиль", "форматирование"],
     "id_author": 1,
     "id_card": 1,
     "upload_date": "2023-01-15",
     "views_count": 100,
     "favorites_count": 25
     },
    {"question": "Как объявить список в Python?",
     "answer": "С помощью квадратных скобок: lst = []",
     "category": "Основы",
     "tags": ["списки", "основы"],
     "id_author": 2,
     "id_card": 2,
     "upload_date": "2023-01-20",
     "views_count": 150,
     "favorites_count": 30
     },
    {"question": "Что делает метод .append()?",
     "answer": "Добавляет элемент в конец списка.",
     "category": "Списки",
     "tags": ["списки", "методы"],
     "id_author": 2,
     "id_card": 3,
     "upload_date": "2023-02-05",
     "views_count": 75,
     "favorites_count": 20
     },
    {"question": "Какие типы данных в Python иммутабельные?",
     "answer": "Строки, числа, кортежи.",
     "category": "Типы данных",
     "tags": ["типы данных", "иммутабельность"],
     "id_author": 1,
     "id_card": 4,
     "upload_date": "2023-02-10",
     "views_count": 90,
     "favorites_count": 22
     },
    {"question": "Как создать виртуальное окружение в Python?",
     "answer": "С помощью команды: python -m venv myenv",
     "category": "Виртуальные окружения",
     "tags": ["venv", "окружение"],
     "id_author": 2,
     "id_card": 5,
     "upload_date": "2023-03-01",
     "views_count": 120,
     "favorites_count": 40
     }
]
info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ],
    "cards": cards_dataset}


def main(request):
    """
    Функция для отображения главной страницы
    будет возвращать рендер шаблона main.html
    """
    return render(request, 'main.html', context=info)


def about(request):
    """
    Функция для отображения страницы о сайте
    будет возвращать рендер шаблона about.html
    """
    return render(request, 'about.html', context=info)


def catalog(request):
    """
    Функция для отображения каталога карточек
    будет возвращать рендер шаблона cards/catalog.html
    """

    sort = request.GET.get('sort', 'upload_date')
    order = request.GET.get('order', 'desc')

    valid_sort_fields = {'upload_date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'upload_date'

    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    cards = Card.objects.all().order_by(order_by)
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu']
    }
    return render(request, 'cards/catalog.html', context)


def get_category_by_name(request, slug):
    """
    Функция для отображения категорий по имени
    """
    return HttpResponse(f"Категория {slug}")


def get_detail_card_by_id(request, card_id):
    """
    Функция для отображения детального представления карточки
    будет возвращать рендер шаблона cards/card_detail.html
    """
    card = Card.objects.get(pk=card_id)
    context = {
        'card': card,
        'menu': info['menu']
    }

    return render(request, 'cards/card_detail.html', context)
