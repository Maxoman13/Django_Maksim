from django import forms
from .models import Categories, Card, Tag
from django.core.exceptions import ValidationError
import re


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=100)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label='Категория',
                                      empty_label='Выберите категорию', required=True)