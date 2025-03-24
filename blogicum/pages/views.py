from django.shortcuts import render  # Функция для рендера шаблонов, чтобы показывать HTML
from django.views.generic import TemplateView  # Класс для простых страниц, где просто шаблон нужен

# Класс для страницы "О нас"
class About(TemplateView):
    template_name = 'pages/about.html'  # Указываем шаблон, который будет показан

# Класс для страницы "Правила"
class Rules(TemplateView):
    template_name = 'pages/rules.html'  # Шаблон для правил
    # Тоже самое, что и About, только другой файл

# Функция для ошибки 404
def page_not_found(request, exception):
    # request - запрос, exception - причина ошибки
    return render(request, 'pages/404.html', status=404)  # Показываем страницу 404 с кодом 404
    # Django его передаёт автоматически

# Функция для ошибки CSRF
def csrf_failure(request, reason=''):
    # reason - причина ошибки, но тут не используем
    return render(request, 'pages/403csrf.html', status=403)  # Показываем страницу с кодом 403
    # в settings.py через CSRF_FAILURE_VIEW

# Функция для ошибки 500
def server_error(request):
    # Просто показываем страницу, когда сервер сломался
    return render(request, 'pages/500.html', status=500)  # Код 500 для серверных ошибок
