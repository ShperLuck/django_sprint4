from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.models import Post, Comment

User = get_user_model()

class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""
    class Meta:
        model = Comment
        fields = ('text',)

class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов"""
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }

class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя с дополнительным полем 'bio'"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'bio')

class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'bio')  # Добавляем bio

class PasswordChangeForm(forms.Form):
    """Форма для смены пароля"""
    password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
