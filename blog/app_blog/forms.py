from django import forms
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from blog.settings import POSTS_FILE_DELIMITER, POST_MAX_LENGTH

create_form_help_text = format_lazy('{start} {length} {end}', start=_('No more than'),
                                    length=POST_MAX_LENGTH, end=_('characters'))

create_posts_from_file_help_text = format_lazy('{start}{delimiter}{middle}{delimiter}{end}',
                                               start=_('One post = one line. Line format: (Title)'),
                                               delimiter=POSTS_FILE_DELIMITER, middle=_('(Content)'),
                                               end=_('(Publication date). Publication date in the format hh:mi:ss dd.mm.yyyy'))


class CreatePostForm(forms.Form):
    """Форма для создания поста"""
    post_title = forms.CharField(max_length=70, label=_('Post title'), help_text=_('No more than 70 characters'),
                                 required=True)
    post_content = forms.CharField(max_length=POST_MAX_LENGTH, widget=forms.Textarea, label=_('Post content'),
                                   help_text=create_form_help_text, required=True)
    images_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label=_('Images'),
                                    required=False)


class CreatePostsFromFileForm(forms.Form):
    """Форма для создания списка постов из файла"""
    posts_file = forms.FileField(label=_('Post List File'),
                                 help_text=create_posts_from_file_help_text)
