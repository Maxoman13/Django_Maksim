from datetime import datetime
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Card
from .forms import CardForm, SearchForm
from django.views.generic import TemplateView

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
    "cards_count": len('cards'),
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


class MenuMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        return context


class IndexView(MenuMixin, TemplateView):
    template_name = 'main.html'


class AboutView(MenuMixin, TemplateView):
    template_name = 'about.html'

    extra_context = {'title': 'О проекте'}


def catalog(request):
    """
    Функция для отображения каталога карточек
    будет возвращать рендер шаблона cards/catalog.html
    """

    sort = request.GET.get('sort', 'upload_date')
    order = request.GET.get('order', 'desc')
    search_query = request.GET.get('search_query', '')

    valid_sort_fields = {'upload_date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'upload_date'

    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    if not search_query:
        cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
    else:
        cards = Card.objects.filter(Q(question__icontains=search_query) |
                                    Q(answer__icontains=search_query) |
                                    Q(tags__name__icontains=search_query)).select_related('category').prefetch_related(
            'tags').order_by(order_by).distinct()

    context = {
        'cards': cards,
        'cards_count': len(cards),
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


def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    # Добываем карточки из БД по тегу
    cards = Card.objects.filter(tags__id=tag_id)

    # Подготавливаем контекст и отображаем шаблон
    context = {
        'cards': cards,
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)


def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save()
            return redirect(card.get_absolute_url())
    else:
        form = CardForm()

    return render(request, 'cards/add_card.html', {'form': form})
