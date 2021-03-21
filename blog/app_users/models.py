from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_media.models import ProfileAvatarImage


class Profile(models.Model):
    """Расширешие модели пользователя, для хранения аватарки"""
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE)
    avatar_image_file = models.ForeignKey(ProfileAvatarImage, null=True, verbose_name=_('user profile avatar'),
                                          on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

