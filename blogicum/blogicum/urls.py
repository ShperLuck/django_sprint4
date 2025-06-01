from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from blog.forms import CustomUserCreationForm

app_name = 'blogicum'


class RegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию на Блогикум.',
            'from@example.com',
            [user.email],
            fail_silently=True,
        )
        return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', RegistrationView.as_view(), name='registration'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
