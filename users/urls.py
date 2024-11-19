from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.views import UserCreateView, email_verification, UserResetPasswordView, NotMailPageView
# from django.views.decorators.cache import cache_page

from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset_password'),
    path('not-mail/', NotMailPageView.as_view(), name='not_mail'),
 ]
