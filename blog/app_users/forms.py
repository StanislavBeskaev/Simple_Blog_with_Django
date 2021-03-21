from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app_media.models import ProfileAvatarImage


class RegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""
    first_name = forms.CharField(max_length=30, required=False, label=_('First name'))
    last_name = forms.CharField(max_length=30, required=False, label=_('Second name'))
    email = forms.EmailField(required=False, label=_('Email'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')


class UserAccountEditForm(forms.ModelForm):
    """Форма для редактирования данных пользователя"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UploadProfileAvatarImageForm(forms.ModelForm):
    class Meta:
        model = ProfileAvatarImage
        fields = ['avatar_image_file']

