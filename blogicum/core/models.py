from django.db import models  # Модуль для работы с моделями, это как таблицы в базе данных

# Базовая модель для публикаций
class PublishedModel(models.Model):
    # Поле, чтобы показывать или скрывать запись
    is_published = models.BooleanField(
        default=True,  # По умолчанию True, значит опубликовано
        verbose_name='Опубликовано',  # Название в админке
        help_text='Снимите галочку, чтобы скрыть публикацию.',  # Подсказка в админке
    )  # BooleanField - это да/нет, типа галочка
    
    # Поле для даты и времени создания
    created_at = models.DateTimeField(
        auto_now_add=True,  # Автоматически ставит дату при создании
        verbose_name='Добавлено'  # Название в админке
    )  # DateTimeField - это поле для даты и времени

    # Настройки модели
    class Meta:
        abstract = True  # Делаем модель абстрактной, чтобы её нельзя было создать напрямую, только наследовать
