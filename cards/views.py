from datetime import datetime
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Card
from .forms import CardForm, SearchForm
from django.views.generic import TemplateView, ListView

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

    @staticmethod
    def get_cards_count():
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count)

        return cards_count


class IndexView(MenuMixin, TemplateView):
    template_name = 'main.html'


class AboutView(MenuMixin, TemplateView):
    template_name = 'about.html'


class CatalogView(ListView):
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 30  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__icontains=search_query) |
                Q(answer__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct().order_by(order_by)
        else:
            queryset = Card.objects.all().order_by(order_by)
        return queryset

    # Метод для добавления дополнительного контекста
    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        # Добавление статических данных в контекст, если это необходимо
        context['menu'] = info['menu']  # Пример добавления статических данных в контекст
        context['cards_count'] = self.get_cards_count()
        return context

    @staticmethod
    def get_cards_count():
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count)

        return cards_count

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
