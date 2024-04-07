from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в админке
    list_display = ('id', 'question', 'answer', 'category', 'views', 'upload_date')

    list_display_links = ('id',)

    list_filter = ('category', 'upload_date')
