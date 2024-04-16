from django.contrib import admin
from django.urls import path
from cards import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.get_category_by_name, name='category_by_name'),
    path('<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
    path('tags/<int:tag_id>/',  views.get_cards_by_tag, name='cards_by_tag'),
    path('add_card/', views.add_card, name='add_card'),
]
