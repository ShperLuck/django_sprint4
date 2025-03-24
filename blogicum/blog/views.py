from django.utils import timezone  # Это модуль для работы с датой и временем, чтобы проверять даты постов
from django.views.generic import (
    CreateView, UpdateView, DetailView)  # Готовые классы Django: CreateView - для создания объектов, UpdateView - для редактирования, DetailView - для показа деталей
from django.urls import reverse_lazy  # Функция для создания ссылок, "ленивая" - генерирует их только когда нужно
from django.core.paginator import Paginator  # Класс для деления списка постов на страницы, чтобы не показывать всё сразу
from django.contrib.auth.decorators import login_required  # Декоратор, чтобы доступ был только у залогиненных пользователей
from django.contrib.auth.mixins import LoginRequiredMixin  # То же самое, но как примесь для классов
from django.shortcuts import render, get_object_or_404, redirect  # Удобные функции: render - рендерит шаблон, get_object_or_404 - ищет объект или даёт 404, redirect - перенаправляет
from django.contrib.auth import update_session_auth_hash  # Функция, чтобы сессия оставалась активной после смены пароля
from django.contrib.auth import get_user_model  # Получаем модель пользователя, которая используется в проекте
from django.http import Http404  # Ошибка 404 для случаев, когда что-то не найдено
from django.http import HttpResponseForbidden  # Ошибка 403, если у пользователя нет прав

from blog.forms import PostForm, CommentForm, ProfileForm, PasswordChangeForm  # Импортируем наши формы из файла forms.py
from blog.models import Post, Category, Comment  # Модели блога: посты, категории, комментарии
from blogicum.settings import LIMIT_POSTS  # Константа с лимитом постов на страницу из настроек

User = get_user_model()  # Сразу берём модель пользователя, чтобы использовать её в коде


def profile_view(request, username):
    # Функция для отображения профиля пользователя
    # request - это запрос от браузера, username - имя пользователя из URL
    user = get_object_or_404(User, username=username)  # Ищем пользователя по имени, если нет - ошибка 404
    posts = user.posts.all()  # Берём все посты этого пользователя через связь в модели (related_name='posts')
    current_time = timezone.now()  # Получаем текущее время, чтобы сравнивать с датами публикации
    if request.user.username != username:  # Если это не мой профиль
        posts = posts.filter(  # Фильтруем посты: только опубликованные, с опубликованными категориями и датой до текущего момента
            is_published=True,  # Пост должен быть опубликован
            category__is_published=True,  # Категория тоже должна быть активной (двойное подчёркивание - это связь через модель)
            pub_date__lte=current_time,  # Дата публикации меньше или равна текущей (__lte значит "less than or equal")
        )
    # Пагинация - это когда мы делим длинный список на страницы, чтобы грузилось быстрее
    paginator = Paginator(posts, LIMIT_POSTS)  # Создаём объект пагинации с лимитом постов
    page_number = request.GET.get('page')  # Берём номер страницы из запроса, например ?page=2
    page_obj = paginator.get_page(page_number)  # Получаем конкретную страницу с постами
    context = {'profile': user, 'page_obj': page_obj}  # Словарь с данными для шаблона
    return render(request, 'blog/profile.html', context)  # Рендерим шаблон с этим контекстом


def password_change_view(request, username):
    # Функция для смены пароля
    # Это не класс, а обычная функция, потому что логика чуть сложнее стандартной
    user = request.user  # Текущий пользователь из запроса
    form = PasswordChangeForm(user, request.POST)  # Создаём форму с данными из POST-запроса
    if request.method == 'POST' and form.is_valid():  # Если это POST и форма заполнена правильно
        user = form.save()  # Сохраняем новый пароль
        update_session_auth_hash(request, user)  # Обновляем сессию, чтобы пользователя не выкинуло из аккаунта
        return redirect('blog:password_change_done')  # Перенаправляем на страницу успеха
    else:
        form = PasswordChangeForm(user)  # Если не POST, показываем пустую форму
    context = {'form': form}  # Контекст для шаблона
    return render(request, 'blog/password_change_form.html', context)  # Рендерим страницу с формой


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    # Класс для редактирования профиля
    # LoginRequiredMixin - примесь, которая проверяет, что пользователь залогинен
    model = User  # Работаем с моделью пользователя
    form_class = ProfileForm  # Используем нашу форму для профиля
    template_name = 'blog/user.html'  # Шаблон для этой страницы

    def get_object(self, queryset=None):
        # Метод, чтобы взять объект для редактирования
        # Переопределяем, чтобы редактировать только свой профиль
        return self.request.user  # Возвращаем текущего пользователя

    def get_success_url(self):
        # Метод для ссылки после успешного редактирования
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})  # Возвращаемся в профиль


class PostMixin:
    # Класс с общими настройками для работы с постами
    # Используем его, чтобы не повторять код в других классах
    model = Post  # Модель постов
    form_class = PostForm  # Форма для постов
    template_name = 'blog/create.html'  # Шаблон для создания и редактирования


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    # Класс для создания нового поста
    # CreateView - это готовый класс Django для создания объектов
    pk_url_kwarg = 'post_id'  # Имя аргумента из URL, хотя тут он не особо нужен

    def form_valid(self, form):
        # Метод вызывается, когда форма заполнена правильно
        form.instance.author = self.request.user  # Устанавливаем автора как текущего пользователя
        return super().form_valid(form)  # Вызываем родительский метод для сохранения


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    # Класс для редактирования поста
    pk_url_kwarg = 'post_id'  # Имя аргумента из URL (id поста)

    def dispatch(self, request, *args, **kwargs):
        # Метод для проверки перед обработкой запроса
        if self.get_object().author != self.request.user:  # Если я не автор поста
            return redirect('blog:post_detail', self.kwargs['post_id'])  # Перекидываем на страницу деталей
        return super().dispatch(request, *args, **kwargs)  # Если автор, продолжаем

    def get_context_data(self, **kwargs):
        # Метод для добавления данных в контекст шаблона
        context = super().get_context_data(**kwargs)  # Берём стандартный контекст
        context['is_edit'] = True  # Добавляем флаг, чтобы шаблон знал, что это редактирование
        return context


@login_required
def delete_post(request, post_id):
    # Функция для удаления поста
    template_name = 'blog/create.html'  # Используем тот же шаблон, что для создания
    delete_post = get_object_or_404(Post, pk=post_id, author__username=request.user)  # Ищем пост по id и автору
    if request.method != 'POST':  # Если это GET-запрос
        context = {'post': delete_post, 'is_delete': True}  # Показываем подтверждение удаления
        return render(request, template_name, context)
    if delete_post.author == request.user:  # Проверяем, что я автор
        delete_post.delete()  # Удаляем пост
    return redirect('blog:profile', request.user)  # Возвращаемся в профиль


class PostDetailView(DetailView):
    # Класс для отображения деталей поста
    model = Post  # Работаем с моделью постов
    template_name = 'blog/detail.html'  # Шаблон для страницы
    context_object_name = 'post'  # Имя объекта в шаблоне
    pk_url_kwarg = 'post_id'  # Имя аргумента из URL

    def get_object(self):
        # Метод для получения поста
        object = super().get_object()  # Берём пост по id
        if self.request.user != object.author and (not object.is_published or not object.category.is_published):
            # Если я не автор и пост или категория не опубликованы
            raise Http404()  # Выдаём ошибку 404
        return object

    def get_context_data(self, **kwargs):
        # Добавляем данные в контекст
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Форма для нового комментария
        context['comments'] = self.object.comments.select_related('author')  # Комментарии с авторами (select_related ускоряет запрос)
        return context


def index(request):
    # Главная страница с постами
    template = 'blog/index.html'
    current_time = timezone.now()  # Текущее время
    post = Post.objects.select_related('category').filter(  # Берём посты с категориями
        pub_date__lte=current_time,  # Только до текущей даты
        is_published=True,  # Опубликованные
        category__is_published=True,  # С опубликованными категориями
    )
    paginator = Paginator(post, LIMIT_POSTS)  # Делим на страницы
    page_number = request.GET.get('page')  # Номер страницы из запроса
    page_obj = paginator.get_page(page_number)  # Объект страницы
    context = {'page_obj': page_obj}
    return render(request, template, context)


def category_posts(request, category_slug):
    # Страница с постами по категории
    template = 'blog/category.html'
    current_time = timezone.now()
    category = get_object_or_404(Category, slug=category_slug, is_published=True)  # Ищем категорию по slug
    post_list = category.posts.select_related('category').filter(  # Посты этой категории
        is_published=True,
        pub_date__lte=current_time,
    )
    paginator = Paginator(post_list, LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    # Добавление комментария
    post = get_object_or_404(Post, pk=post_id)  # Ищем пост
    form = CommentForm(request.POST)  # Форма с данными из запроса
    if form.is_valid():  # Если форма заполнена правильно
        comment = form.save(commit=False)  # Создаём объект, но не сохраняем в базу
        comment.author = request.user  # Устанавливаем автора
        comment.post = post  # Привязываем к посту
        comment.save()  # Теперь сохраняем
    return redirect('blog:post_detail', post_id)  # Перенаправляем на страницу поста


@login_required
def edit_comment(request, post_id, comment_id):
    # Редактирование комментария
    comment = get_object_or_404(Comment, id=comment_id)  # Ищем комментарий
    if comment.author != request.user:  # Если я не автор
        return HttpResponseForbidden('У вас нет прав для редактирования этого комментария.')
    if request.method == 'POST':  # Если отправили форму
        form = CommentForm(request.POST, instance=comment)  # Форма с текущим комментарием
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('blog:post_detail', post_id)
    else:
        form = CommentForm(instance=comment)  # Показываем форму с данными комментария
    context = {'form': form, 'comment': comment, 'is_edit': True}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    # Удаление комментария
    comment = get_object_or_404(Comment, id=comment_id)  # Ищем комментарий
    if comment.author != request.user:  # Если я не автор
        return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")
    if request.method == "POST":  # Если подтвердили удаление
        comment.delete()  # Удаляем
        return redirect('blog:post_detail', post_id)
    context = {'comment': comment, 'is_delete': True}  # Показываем подтверждение
    return render(request, 'blog/comment.html', context)