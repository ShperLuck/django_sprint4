from django.urls import include, path, reverse_lazy  # include - подключает другие URL, path - задаёт маршруты, reverse_lazy - ссылки, которые строятся позже
from django.conf import settings  # Берём настройки из settings.py
from django.conf.urls.static import static  # Для работы со статичными файлами
from django.contrib import admin  # Админка от Django
from django.views.generic.edit import CreateView  # Класс для создания объектов, тут для регистрации
from users.forms import CustomUserCreationForm  # Наша форма для регистрации

app_name = 'blogicum'  # Имя приложения, чтобы маршруты не путались

# Список маршрутов (URL)
urlpatterns = [
    path('admin/', admin.site.urls),  # Админка доступна по /admin/
    path('', include('blog.urls', namespace='blog')),  # Главная и блог, подключаем из blog/urls.py, namespace нужен для уникальности
    path('pages/', include('pages.urls', namespace='pages')),  # Статичные страницы из pages/urls.py
    path('auth/', include('django.contrib.auth.urls')),  # Готовые маршруты для авторизации (логин, выход и т.д.)
    path(
        'auth/registration/',  # Путь для регистрации
        CreateView.as_view(  # Используем класс для создания юзера
            template_name='registration/registration_form.html',  # Шаблон формы
            form_class=CustomUserCreationForm,  # Наша кастомная форма
            success_url=reverse_lazy('blog:index'),  # Куда идти после регистрации
        ),
        name='registration',  # Имя маршрута
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Подключаем статичные файлы (CSS, JS)

# Добавляем debug_toolbar, если отладка включена
if settings.DEBUG:  # Проверяем, включён ли DEBUG
    import debug_toolbar  # Панель отладки
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)  # Добавляем её маршрут
    # Сначала не понял, зачем кортеж с запятой, оказалось, для правильного сложения списков

# Подключаем медиафайлы
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Для загружаемых файлов, типа картинок
# Пришлось лезть в settings.py, чтобы найти MEDIA_URL и MEDIA_ROOT

# Обработчики ошибок
handler404 = 'pages.views.page_not_found'  # Страница для 404
handler500 = 'pages.views.server_error'  # Страница для 500