from django.db import models

from app_blog.models import Post
from django.utils.translation import gettext_lazy as _


class ProfileAvatarImage(models.Model):
    """Модель для хранения аватаров профиля пользователя"""
    avatar_image_file = models.ImageField(upload_to='avatar_images/', verbose_name=_('picture, user profile avatar'))

    def __str__(self):
        return str(self.avatar_image_file)

    class Meta:
        verbose_name = _('profile avatar image')
        verbose_name_plural = _('profile avatar images')


class PostImage(models.Model):
    """Модель для хранения картинок постов"""
    post_image_file = models.ImageField(upload_to='post_images/', verbose_name=_('Image for post'))
    post = models.ForeignKey(Post, verbose_name=_('Post'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('post image')
        verbose_name_plural = _('post images')
