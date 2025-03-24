# Подключаем необходимые модули для работы с формами
from django import forms  # Работа с формами в Django
from django.contrib.auth import get_user_model  # Получаем текущую модель пользователя
from django.contrib.auth.forms import UserCreationForm  # Готовая форма для регистрации пользователей
from blog.models import Post, Comment  # Импортируем модели постов и комментариев из приложения blog

# Получаем модель пользователя
User = get_user_model() 


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""
    class Meta:
        model = Comment  # Привязываем форму к модели Comment
        fields = ('text',)  # Указываем, что в форме будет только поле 'text' (!запятая нужна, т.к. это кортеж!)


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов"""
    class Meta:
        model = Post  # Привязываем форму к модели Post
        exclude = ('author',)  # Исключаем поле 'author', по идеи будет автоматом
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})  # Поле даты с календариком для выбора
        }


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя с дополнительным полем 'bio'"""
    class Meta(UserCreationForm.Meta):  # Тут от стандартной формы UserCreationForm
        model = User  # Используем нашу модель пользователя
        fields = ('username', 'bio')  # Добавляем к стандартному набору полей ещё и 'bio'


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User  # Привязываем форму к модели пользователя
        fields = ('first_name', 'last_name', 'username', 'email')  # Доступные для редактирования поля профиля


class PasswordChangeForm(forms.Form):
    """Форма для смены пароля"""
    password1 = forms.CharField(
        label='New password',  # Подпись для поля
        widget=forms.PasswordInput  #  скрытие ввода пароля
    )
    password2 = forms.CharField(
        label='Confirm new password',  # Подпись для подтверждения пароля
        widget=forms.PasswordInput  # Скрытый ввод
    )

    def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()  # Получаем очищенные данные из формы
        password1 = cleaned_data.get('password1')  #  первый пароль
        password2 = cleaned_data.get('password2')  # второй пароль

        if password1 and password2 and password1 != password2:  # Если оба пароля введены и не совпадают
            raise forms.ValidationError("Passwords don't match")  # Вызываем ошибку валидации

        return cleaned_data  
