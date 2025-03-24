# Импортируем базовый класс для конфигурации приложений
from django.apps import AppConfig

# Создаём класс "blog"
class BlogConfig(AppConfig):
    # Настроим тип автоинкрементного поля по умолчанию
    # Используем BigAutoField, чтобы поле могло хранить больше значений
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Указываем техническое имя приложения
    name = 'blog'
    
    # имя для отображения в админке
    verbose_name = 'Блог'