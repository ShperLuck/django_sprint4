# Импортируем нужные модули Django
from django.db import models  # Это модуль для работы с базой данных через Django ORM (Object-Relational Mapping)
from django.contrib.auth import get_user_model  # Получаем модель пользователя (может быть кастомной)
from django.urls import reverse  # Функция для построения URL-адресов

from core.models import PublishedModel  # Наследуемый класс, возможно, содержит общие поля (например, дата публикации)

# Получаем модель пользователя, которую использует проект
User = get_user_model()


class Category(PublishedModel):
    """Класс модели для категорий постов"""
    title = models.CharField(max_length=256, verbose_name='Заголовок')  # Поле заголовка категории (до 256 символов)
    description = models.TextField(verbose_name='Описание')  # Поле для описания категории (без ограничения длины)
    image = models.ImageField('Фото', upload_to='post_images', blank=True)  
    # Поле для загрузки изображения (можно оставить пустым, blank=True)

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )  # Slug — уникальная строка для URL (например, "news" вместо ID)

    class Meta:
        verbose_name = 'категория'  # Как будет отображаться в админке (единичное число)
        verbose_name_plural = 'Категории'  # Как будет отображаться во множественном числе

    def __str__(self):
        return self.title  # При выводе объекта в строку (например, в админке) будет показываться заголовок категории


class Location(PublishedModel):
    """Класс модели для местоположения"""
    name = models.CharField(max_length=256, verbose_name='Название места')  # Название места (например, город или страна)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name  # Отображение объекта в виде названия места


class Post(PublishedModel):
    """Класс модели для постов (статей)"""
    title = models.CharField(max_length=256, verbose_name='Заголовок')  # Заголовок статьи
    text = models.TextField(verbose_name='Текст')  # Основной текст статьи (без ограничений по длине)
    image = models.ImageField('Фото', upload_to='post_images', blank=True)  
    # Поле для изображения, можно оставить пустым

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.',
    )  # Дата публикации. Позволяет делать отложенные публикации

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Если пользователь удаляется, его посты тоже удаляются
        verbose_name='Автор публикации',
        related_name='posts',  # Связываем с пользователем, чтобы можно было получить user.posts.all()
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,  # Если локацию удалят, в этом поле останется NULL
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # Если категорию удалят, в этом поле останется NULL
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)  # Сортировка постов по дате публикации (сначала новые)

    def get_absolute_url(self):
        """Функция возвращает URL профиля автора поста"""
        return reverse('blog:profile', args=[self.author])

    def comment_count(self):
        """Метод для подсчёта количества комментариев у поста"""
        return self.comments.count()  # Django автоматически создаст связь по related_name='comments'

    def __str__(self):
        return self.title  # Отображение объекта в виде заголовка поста


class Comment(models.Model):
    """Класс модели для комментариев"""
    text = models.TextField('Текст комментария')  # Основной текст комментария
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # Если пост удалят, комментарии тоже удалятся
        related_name='comments',  # Связываем с постом, чтобы можно было получить post.comments.all()
        verbose_name='Пост',
        help_text='Выберите пост, к которому относится комментарий',
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания комментария автоматом вроде
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Если пользователь удаляется, удаляются и его комментарии
        related_name='author',  # Куча конфликтов
    )

    class Meta:
        ordering = ('created_at',)  # Сортировка комментариев по дате (старые сверху)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text  # Показывать текст комментария в админке


class Profile(PublishedModel):
    """Класс модели для профиля пользователя"""
    first_name = models.CharField(max_length=30, blank=True)  # Имя (может быть пустым)
    last_name = models.CharField(max_length=30, blank=True)  # Фамилия (может быть пустой)
    email = models.EmailField(blank=True)  # Email (может быть пустым)
    address = models.CharField(max_length=100, blank=True)  # Адрес (может быть пустым)

    def __str__(self):
        return self.title  # Ошибка: у модели нет поля title! Возможно, нужно вернуть self.first_name
