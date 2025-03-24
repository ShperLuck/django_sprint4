from pathlib import Path  # Модуль для работы с путями к файлам

# Базовая папка проекта
BASE_DIR = Path(__file__).resolve().parent.parent  # Путь к корню проекта от этого файла


# Настройки для разработки
SECRET_KEY = (
    'django-insecure-towmz)2=!8fc=7is8b2&-o0mecab!+dkqbd53^t#)%_rjzybxq'
)  # Ключ для шифрования, на продакшене надо менять

DEBUG = True  # Режим отладки, показывает ошибки в браузере

ALLOWED_HOSTS = [
    'localhost',  # Локальный хост
    '127.0.0.1',  # IP для локалки
]  # Где сайт работает


# Приложения проекта
INSTALLED_APPS = [
    'django_bootstrap5',  # Bootstrap для стилей
    'blog.apps.BlogConfig',  # Наше приложение blog
    'pages.apps.PagesConfig',  # Приложение для страниц
    'core.apps.CoreConfig',  # Базовое приложение
    'users.apps.UsersConfig',  # Приложение с юзерами
    'django.contrib.admin',  # Админка
    'django.contrib.auth',  # Авторизация
    'django.contrib.contenttypes',  # Связь моделей
    'django.contrib.sessions',  # Сессии
    'django.contrib.messages',  # Сообщения
    'django.contrib.staticfiles',  # Статические файлы
    'debug_toolbar',  # Панель отладки
]


# Middleware - обработка запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',  # Сессии
    'django.middleware.common.CommonMiddleware',  # Общие штуки
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Кто залогинен
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от кликов
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Отладка
]

INTERNAL_IPS = [
    '127.0.0.1',  # IP для debug_toolbar
]

POSTS_PER_PAGE = 5  # Сколько постов на странице

ROOT_URLCONF = 'blogicum.urls'  # Главный файл с URL

# Папка с шаблонами
TEMPLATES_DIR = BASE_DIR / 'templates'  # Путь к templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Движок шаблонов
        'DIRS': [TEMPLATES_DIR],  # Где искать шаблоны
        'APP_DIRS': True,  # Искать в приложениях
        'OPTIONS': {
            'context_processors': [  # Добавляют данные в шаблоны
                'django.template.context_processors.debug',  # Отладка
                'django.template.context_processors.request',  # Request
                'django.contrib.auth.context_processors.auth',  # Юзер
                'django.contrib.messages.context_processors.messages',  # Сообщения
            ],
        },
    },
]

WSGI_APPLICATION = 'blogicum.wsgi.application'  # Файл для сервера


# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite для разработки
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к базе
    }
}


# Проверка паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Не похож на имя
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # Минимальная длина
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # Не простой
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # Не только цифры
]


# Язык и время
LANGUAGE_CODE = 'ru-RU'  # Русский язык
TIME_ZONE = 'UTC'  # Часовой пояс
USE_I18N = True  # Поддержка языков
USE_L10N = True  # Локализация
USE_TZ = True  # Часовые пояса


# Статические файлы
STATIC_URL = '/static/'  # URL для CSS и JS

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',  # Папка для статичных файлов
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Тип ID в моделях

# Свои настройки (добавили сами):
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'  # Страница ошибки CSRF

AUTH_USER_MODEL = 'users.MyUser'  # Наша модель юзера

LOGIN_REDIRECT_URL = 'blog:index'  # Куда после логина

MEDIA_ROOT = BASE_DIR / 'media'  # Папка для файлов юзеров

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'  # Письма в файлы
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  # Куда сохранять письма

LOGIN_URL = 'login'  # Страница логина

LIMIT_POSTS = 10  # Лимит постов на странице