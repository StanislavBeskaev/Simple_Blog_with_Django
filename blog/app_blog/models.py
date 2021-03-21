from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    """Модель для поста блога"""
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Post author'))
    publication_date = models.DateTimeField(verbose_name=_('Post publication date'))
    post_title = models.CharField(max_length=70, verbose_name=_('Post title'), null=False)
    post_content = models.TextField(verbose_name=_('Post content'), null=False)

    def __str__(self):
        return f'id={self.id}, {self.post_title}'

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
