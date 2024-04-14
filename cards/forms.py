from django import forms
from .models import Categories, Card, Tag
from django.core.exceptions import ValidationError
import re


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=100)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea)
