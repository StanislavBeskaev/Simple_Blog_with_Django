from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.utils.translation import gettext as _

from core.handlers import get_correct_file_path_to_img_tag
from .forms import RegisterForm, UserAccountEditForm, UploadProfileAvatarImageForm
from .models import Profile


class LoginView(LoginView):
    template_name = 'login.html'


class LogoutView(LogoutView):
    template_name = 'logout.html'


def register_view(request):
    """Вью для страницы регистрации"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # "сырой" пароль
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/blog/post_list')

    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, template_name='register.html', context=context)


def user_account_view(request):
    """Вью для страницы информации о пользователе"""
    if not request.user.is_authenticated:
        raise PermissionDenied()
    context = {}
    if request.user.profile.avatar_image_file:
        avatar_path = get_correct_file_path_to_img_tag(request.user.profile.avatar_image_file)
        context['avatar_path'] = avatar_path

    return render(request, 'account.html', context)


class UserAccountEditView(generic.TemplateView):
    """Вью для страницы редактировния данных пользователя"""
    template_name = 'edit_account.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_account_edit_form = UserAccountEditForm(instance=self.request.user)
            context['edit_form'] = user_account_edit_form
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            user_account_edit_form = UserAccountEditForm(request.POST, instance=request.user)
            context['edit_form'] = user_account_edit_form
            if user_account_edit_form.is_valid():
                user_account_edit_form.save()
                context['message'] = _('Changes saved!')
            else:
                context['message'] = _('Please enter correct data')

        return render(request, self.template_name, context)


def upload_avatar_image_view(request):
    """Вью для страницы загрузки аватарки пользовалеля"""

    if not request.user.is_authenticated:
        raise PermissionDenied()

    if request.method == 'POST':
        avatar_upload_form = UploadProfileAvatarImageForm(request.POST, request.FILES)
        if avatar_upload_form.is_valid():
            avatar_upload_form.save()
            profile = request.user.profile
            profile.avatar_image_file = avatar_upload_form.instance
            profile.save()
            return redirect('account')
        else:
            context = {'edit_form': avatar_upload_form, 'message': _('Specify the correct file')}
            return render(request, 'upload_avatar.html', context)
    else:
        avatar_upload_form = UploadProfileAvatarImageForm()
        context = {'edit_form': avatar_upload_form}
        return render(request, 'upload_avatar.html', context)
