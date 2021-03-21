import datetime

from django.contrib.auth.models import User

from app_blog.models import Post
from app_blog.services.post_services import DATETIME_FORMAT_FOR_DATETIME
from app_users.models import Profile
from blog.settings import POSTS_FILE_DELIMITER

TEST_USERNAME = 'test'
TEST_USER_PASSWORD = 'p@ssw0rd'
TEST_USER_FIRST_NAME = 'first name'
TEST_USER_LAST_NAME = 'last name'
TEST_USER_EMAIL = 'test@test.com'

PUBLICATION_DATETIME_FORMAT = '%H:%M:%S %d.%m.%Y'
TEST_POSTS_LIST_INFO = [{'post_title': 'Первый тестовый пост',
                         'post_content': 'Короткое содержание поста',
                         'publication_date': '12:01:23 03.04.2021'},
                        {'post_title': 'Второй тестовый пост',
                         'post_content': 'Содержание второго поста',
                         'publication_date': '01:01:01 01.01.2011'},
                        {'post_title': 'Как есть бутерброд',
                         'post_content': 'Не пр-равильно ты, дядя Фёдор, бутер-рброд ешь... Ты его колбасой кверху '
                                         'держишь, а надо колбасой на язык класть, м-м-м, так вкуснее получится',
                         'publication_date': '13:13:13 13.08.2013'},
                        ]


def get_list_lines_in_loading_file_format_from_post_list(post_list: list) -> list:
    """Метод принимает список постов post_list и возращает список строк,
     где каждая строка это информация о посте в формате строки загружаемого
      файла для страницы загрузки постов из файла"""
    list_lines = [f'{post.post_title}{POSTS_FILE_DELIMITER}{post.post_content}{POSTS_FILE_DELIMITER}' \
                  f'{post.publication_date.strftime(DATETIME_FORMAT_FOR_DATETIME)}' for post in
                  post_list]
    return list_lines


def get_count_lines_from_file(file_path: str) -> int:
    """Метод возвращает количество строк в файле"""
    return sum(1 for line in open(file_path, 'r'))


def get_list_lines_from_file(file: str) -> list:
    """Метод возращает строки из file, без символа перевода строки в виде списка строк"""
    return [line.split('\n')[0] for line in open(file, 'r', encoding='utf-8')]


def create_test_user() -> User:
    """Метод создающий и возращающий тестового пользователя. Возвращает объект User"""
    user = User.objects.create_user(username=TEST_USERNAME,
                                    password=TEST_USER_PASSWORD,
                                    first_name=TEST_USER_FIRST_NAME,
                                    last_name=TEST_USER_LAST_NAME,
                                    email=TEST_USER_EMAIL)
    Profile.objects.create(user=user)
    return user


def create_test_posts():
    """Метод создающий тестовые посты из константы TEST_POSTS_LIST_INFO"""
    test_user = create_test_user()
    for post_info in TEST_POSTS_LIST_INFO:
        Post.objects.create(
            post_author=test_user,
            post_title=post_info['post_title'],
            post_content=post_info['post_content'],
            publication_date=datetime.datetime.strptime(post_info['publication_date'], PUBLICATION_DATETIME_FORMAT)
        )
