from _csv import reader
from datetime import datetime
from typing import Union

from django.utils.translation import gettext as _

from app_blog.models import Post
from app_media.models import PostImage
from blog.settings import POSTS_FILE_DELIMITER
from core.handlers import get_correct_file_path_to_img_tag

SHORT_CONTENT_LENGTH = 100  # количество символов содержания поста, которые будут отображаться на странице списка постов
DATETIME_FORMAT_FOR_DATETIME = '%H:%M:%S %d.%m.%Y'  # hh:mi:ss dd.mm.yyyy


class PostTitleNullException(Exception):
    pass


class PostContentNullException(Exception):
    pass


def get_post_list() -> list:
    """Метод получения списка постов упорядоченных по дате публикации в порядке убывания"""
    post_list = Post.objects.all().order_by('-publication_date')

    for post in post_list:
        _add_short_content_to_post(post)

    return post_list


def _get_short_content(content: str) -> str:
    """Метод возращает content обрезанный до SHORT_CONTENT_LENGTH символов"""
    if len(content) > SHORT_CONTENT_LENGTH:
        short_content = f'{content[:SHORT_CONTENT_LENGTH]}...'
    else:
        short_content = content
    return short_content


def _add_short_content_to_post(post: Post) -> None:
    """Метод добавления обрезанного содержания для поста.
     Необходим для отображения первых SHORT_CONTENT_LENGTH символов поста на странице списка постов"""
    post.short_content = _get_short_content(post.post_content)


def get_post_images(post: Post) -> Union[list, None]:
    """Метод возрвращет список картинок PostImage или None, если у поста нет картинок"""
    post_image_list = PostImage.objects.filter(post=post)
    if post_image_list:
        for post_image in post_image_list:
            post_image.image_path = get_correct_file_path_to_img_tag(post_image.post_image_file)
    return post_image_list


def create_post(user: str, post_title: str, post_content: str, post_images: list) -> None:
    """Метод создания поста

    :param user: Пользователь автор поста
    :param post_title: Заголовок поста
    :param post_content: Содержание поста
    :param post_images: Список изображений поста
    :return:
    """

    new_post = Post.objects.create(post_author=user,
                                   post_title=post_title,
                                   post_content=post_content,
                                   publication_date=datetime.now())
    if post_images:
        for image in post_images:
            post_image = PostImage(post_image_file=image,
                                   post=new_post)
            post_image.save()


def create_posts_from_file(user, posts_file: str) -> (bool, str):
    """ Метод создания постов из файла

    :param user: Пользователь автор поста
    :param posts_file: Файл со списком постов.Разделитель - значение POSTS_FILE_DELIMITER из настроек.
     Формат файла <Заголовок поста><Содержание><Дата публикации>.Дата публикации в формате hh:mi:ss dd.mm.yyyy'
    :return: Флаг успешности, Сообщение.
    """
    try:
        posts_file_str = posts_file.read().decode('utf-8').split('\n')
        csv_reader = reader(posts_file_str, delimiter=POSTS_FILE_DELIMITER, quotechar='"')
        posts = []
        post_counter = 0
        for row in csv_reader:
            check_post_title(row[0])
            check_post_content(row[1])
            post = Post(post_author=user,
                        post_title=row[0],
                        post_content=row[1],
                        publication_date=datetime.strptime(row[2], DATETIME_FORMAT_FOR_DATETIME)
                        )
            posts.append(post)
            post_counter += 1
        save_posts_in_post_list(posts)
        return True, _('The file was processed successfully.'
                       ' Posted by %(post_counter)s posts') % {'post_counter': post_counter}
    except UnicodeDecodeError:
        return False, _('Posts not created. Error reading file. The file must be text,'
                        ' the delimiter of values is %(delimiter)s') % {'delimiter': POSTS_FILE_DELIMITER}
    except IndexError:
        return False, _('No posts have been created. Not all values are specified '
                        'in line %(line)s') % {'line': post_counter + 1}
    except ValueError:
        return False, _('No posts have been created. Incorrect date value '
                        'in line %(line)s') % {'line': post_counter + 1}
    except PostTitleNullException:
        return False, _('No posts have been created. Empty post title value'
                        ' in line %(line)s') % {'line': post_counter + 1}
    except PostContentNullException:
        return False, _('No posts have been created. Empty post content value'
                        ' in line %(line)s') % {'line': post_counter + 1}
    except Exception:
        return False, _('An unexpected error has occurred')


def save_posts_in_post_list(post_list: list) -> None:
    """Метод сохранения постов в базу из списка постов"""
    for post in post_list:
        post.save()


def check_post_title(post_title: str) -> None:
    """Метод проверки заголовка поста. В случае пустого заголовка вызывается PostTitleNullException"""
    if len(post_title) == 0:
        raise PostTitleNullException


def check_post_content(post_content: str) -> None:
    """Метод проверки содержимого поста. В случае пустого содержимого вызывается PostContentNullException"""
    if len(post_content) == 0:
        raise PostContentNullException
