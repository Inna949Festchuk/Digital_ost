from django.db import models

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

class UsersPromts(models.Model):

    class Meta:
        verbose_name_plural = 'Промты пользователя'
        db_table = "promts_model" # название модели в БД

    usertext = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta: # Индексация поиска
        ordering = ['-created']

    def __str__(self):
        return self.usertext   