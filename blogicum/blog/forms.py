from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Comment, Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введите ваш email.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label='Новый пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Подтверждение пароля', widget=forms.PasswordInput)
