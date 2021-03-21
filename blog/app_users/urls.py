from django.urls import path

from . import views


urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),  # страница авторизации
    path('logout', views.LogoutView.as_view(), name='logout'),  # страница выхода
    path('register', views.register_view, name='register'),  # страница регистрации
    path('account', views.user_account_view, name='account'),  # страница информации о пользователе
    path('edit_account', views.UserAccountEditView.as_view(), name='edit_account'),  # страница редактирования данных пользователя
    path('upload_avatar', views.upload_avatar_image_view, name='upload_avatar'),  # страница загрузки аватарки
]
