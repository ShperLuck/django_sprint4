# Импортируем path, чтобы создавать маршруты
from django.urls import path
# Импортируем views из приложения blog, где находятся обработчики страниц
from blog import views  

# Пространство имён для маршрутов этого приложения
# Нужно, blog и forum
app_name = 'blog'  

# URL-маршруты... 
urlpatterns = [
    # Главная (отображает список постов)
    path('', views.index, name='index'),  

    # показывает посты внутри определённой категории
    # <slug:category_slug> - динамическая часть URL
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts',
    ),

    # Страница профиля пользователя (например: /profile/johndoe/)
    path('profile/<username>/', views.profile_view, name='profile'),

    # Редактирование профиля пользователя
    # <slug:username> — динамический параметр, идентификатор пользователя
    path(
        'profile/<slug:username>/edit_profile/',
        views.ProfileUpdateView.as_view(),  # Используем CBV (класс-представление), нужен . !as_view()!
        name='edit_profile',
    ),

    # Страница создания нового поста 
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),

    # Страница просмотра одного поста
    # <int:post_id> — динамический параметр, идентификатор поста
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),

    # Страница редактирования поста
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),

    # Удаление поста (!!!используется обычное представление, не класс!!!)
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Добавление комментария к посту
    #  тут нет `/` в конце, потому что это действие, а не страница
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),

    # Редактирование комментария
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment',
    ),

    # Удаление комментария
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment',
    ),
]
