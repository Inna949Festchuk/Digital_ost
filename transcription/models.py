from django.db import models
from django.http import HttpResponse
from django.utils.text import slugify

# - - - - - - - - - - - - - - -
# environment на Mac:
# conda activate //anaconda3/envs/condageoenv
# - - - - - - - - - - - - - - -

# Create your models here.
# Выгрузка существующих данных
# python manage.py dumpdata --indent=2 --output=iiassistat_data.json
# Если при выполнении команды вы получаете ошибку кодировки, то включите флаг
# -Xutf8, как показано ниже, чтобы активировать режим Python UTF-8:
# python -Xutf8 manage.py dumpdata --indent=2 --output=iiassistat_data.json
# Загрузка данных в новую базу данных
# python manage.py loaddata iiassistat_data.json

class Commands(models.Model):

    class Meta:
        verbose_name_plural = 'Команды'
        db_table = "commands_model" # название модели в БД

    commands = models.CharField(max_length=250, help_text='Введите команды', verbose_name='Название команды')
    confirmation = models.CharField(max_length=250, help_text='Введите ключевые слова запроса', verbose_name='Ключевые слова запроса')
    slug = models.SlugField(unique=True) # слаг для перехода к выполняемой по команде функции
     
    class Meta: # Индексация поиска
        indexes = [
            models.Index(fields=['commands']),
        ]
    

    # Настраиваем строку поискового вывода из базы данных
    def __str__(self):
        return self.commands


class UsersTexts(models.Model):

    class Meta:
        verbose_name_plural = 'Промты пользователя'
        db_table = "promts_model" # название модели в БД

    usertext = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta: # Индексация поиска
        ordering = ['-created']

    def __str__(self):
        return self.usertext   

class AudioFile(models.Model):
    audio_file = models.FileField(upload_to='audio/%Y/%m/%d')
    # Дополнительные поля, связанные с аудио файлом, могут быть добавлены здесь