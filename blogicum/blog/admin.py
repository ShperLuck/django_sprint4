# Сначала импортируем модули 
from django.contrib import admin
from blog.models import Post, Category, Location

# Реализуем класс для настройки постов в админке
class PostAdmin(admin.ModelAdmin):
    # Тут поля для поиска
    search_fields = (
        'title',    # Поиск по заголовку
        'text',     # Поиск по тексту
        'pub_date', # Поиск по дате
    )

# Создаем класс для категорий
class CategoryAdmin(admin.ModelAdmin):
    search_fields = (
        'title',       # Поиск по названию
        'description', # Поиск по описанию
    )

# для местоположений 
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)

#  отображение пустых значений
admin.site.empty_value_display = 'Не задано'

# Регаем все модели в админке
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)