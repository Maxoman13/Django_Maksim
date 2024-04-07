from django.db import models


class Card(models.Model):
    id = models.AutoField(primary_key=True, db_column='CardId')
    question = models.CharField(max_length=255, db_column='Question')
    answer = models.TextField(max_length=5000, db_column='Answer')
    category_id = models.IntegerField(default=0, db_column='CategoryId')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate')
    views = models.IntegerField(default=0, db_column='Views')
    adds = models.IntegerField(default=0, db_column='Favorites')
    tags = models.ManyToManyField('Tag', through='CardTag', related_name='cards')

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'

    class Meta:
        db_table = 'Cards'  # имя таблицы в базе данных
        verbose_name = 'Карточка'  # имя модели в единственном числе
        verbose_name_plural = 'Карточки'  # имя модели во множественном числе


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagId')
    name = models.CharField(max_length=100, unique=True, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.name}'


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='CategoryId')
    name = models.CharField(max_length=100, unique=True, db_column='Name')

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


class CardTag(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='CardId')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='TagId')

    class Meta:
        db_table = 'CardTags'
        verbose_name = 'Тег карточки'
        verbose_name_plural = 'Теги карточек'

        unique_together = ('card', 'tag')

    def __str__(self):
        return f'Тег {self.tag.name} к карточке {self.card.question}'