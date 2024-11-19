from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
import secrets
from django.core.mail import send_mail
from django.urls import reverse_lazy
from users.forms import UserCreationForm, UserRegisterForm, ResetPasswordForm
from users.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from config.settings import EMAIL_HOST_USER
from users.forms import StyleFormMixin
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth.models import Group


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        group = Group.objects.get(name='users')
        user.groups.add(group)
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserResetPasswordView(PasswordResetView, StyleFormMixin):
    form_class = ResetPasswordForm
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=10)
                user.set_password(password)
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f' Ваш новый пароль {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
            return redirect(reverse('users:login'))
        except:
            return redirect(reverse('users:not_mail'))


class NotMailPageView(TemplateView):
    template_name = "users/not_mail.html"
