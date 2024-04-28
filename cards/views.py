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

info = {
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
    ]}


class MenuMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['cards_count'] = self.get_cards_count()
        return context

    def get_cards_count(self):
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count)

        return cards_count


class IndexView(MenuMixin, TemplateView):
    template_name = 'main.html'


class AboutView(MenuMixin, TemplateView):
    template_name = 'about.html'



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
