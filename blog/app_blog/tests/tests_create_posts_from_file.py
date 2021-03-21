import os
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from app_blog.forms import CreatePostsFromFileForm
from app_blog.models import Post
from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD, get_count_lines_from_file, \
    get_list_lines_from_file, get_list_lines_in_loading_file_format_from_post_list
from blog.settings import POSTS_FILE_DELIMITER


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class CreatePostsFromFileTest(TestCase):
    url_name = 'create_posts_from_file'

    def test_create_posts_from_file_url_forbidden_with_not_authenticated_user(self):
        """Тест запрета доступа к странице создания постов из файла под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 403)

    def _create_test_user_and_login(self):
        """Метод создаёт тестового пользователя и логиниться под ним"""
        create_test_user()
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)

    def test_create_posts_from_file_url_exists_at_desired_location_with_authenticated_user(self):
        """Тест доступности страницы создания постов из файла под авторизованным пользователем"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_create_posts_from_file_uses_correct_template(self):
        """Тест проверяющий, что страница создания постов из файла использует корректный шаблон"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'create_posts_from_file.html')

    def test_create_posts_from_file_header_info(self):
        """Тест проверяющий, что в шапке страницы создания постов из файла есть необходимая информация"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Welcome to the site'))
        self.assertContains(response, _('To the posts list'))
        self.assertContains(response, _('User information'))
        self.assertContains(response, _('Logout'))

    def test_create_posts_from_file_form(self):
        """Тест проверяющий форму создания постов из файла, заголовок, название кнопки """
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Creating posts from a file'))
        self.assertContains(response, _('Create posts'))
        self.assertIn(member='form', container=response.context)
        create_posts_form = response.context['form']
        self.assertTrue(isinstance(create_posts_form, CreatePostsFromFileForm))

    def test_create_posts_from_file_incorrect_file_format(self):
        """Страница создания постов из файла, тест проверющий что посты не создаются если загружается текстовый файл
         некорректного формата"""
        self._create_test_user_and_login()
        incorrect_file_format_path = os.path.normpath(
            os.path.join(os.getcwd(), 'app_blog/tests/test_files/incorrect_file_format.txt'))

        with open(incorrect_file_format_path, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты с некоректным текстовым файлом
            response = self.client.post(reverse(self.url_name), post_context)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверка, что посты не создались
        self.assertEqual(len(list(Post.objects.all())), 0)

        # Отобразилось сообщение об ошибке
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('No posts have been created. Not all values are'
                                                        ' specified in line %(line)s') % {'line': 1})

    def test_create_posts_from_file_img_file(self):
        """Страница создания постов из файла, тест проверющий что посты не создаются если загружается файл
        изображения"""
        self._create_test_user_and_login()
        img_file = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test_image_1.jpg'))

        with open(img_file, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты из файла изображения
            response = self.client.post(reverse(self.url_name), post_context)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверка, что посты не создались
        self.assertEqual(len(list(Post.objects.all())), 0)

        # Проверки, что отобразилось сообщение об ошибке
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _("Posts not created. Error reading file. The file must"
                                                        " be text, the delimiter of values "
                                                        "is %(delimiter)s") % {'delimiter': POSTS_FILE_DELIMITER})

    def test_create_posts_from_file_incorrect_date(self):
        """Страница создания постов из файла, тест проверющий что посты не создаются если загружается текстовый файл
         с некоректно указанной датой"""
        self._create_test_user_and_login()
        incorrect_date_path = os.path.normpath(
            os.path.join(os.getcwd(), 'app_blog/tests/test_files/incorrect_date.txt'))

        with open(incorrect_date_path, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты с некоректным текстовым файлом
            response = self.client.post(reverse(self.url_name), post_context)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверка, что посты не создались
        self.assertEqual(len(list(Post.objects.all())), 0)

        # Отобразилось сообщение об ошибке
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('No posts have been created. Incorrect date value'
                                                        ' in line %(line)s') % {'line': 1})

    def test_create_posts_from_file_empty_title(self):
        """Страница создания постов из файла, тест проверющий что посты не создаются если загружается текстовый файл
         c пустым заголовком поста"""
        self._create_test_user_and_login()
        empty_title_file_path = os.path.normpath(
            os.path.join(os.getcwd(), 'app_blog/tests/test_files/empty_title.txt'))

        with open(empty_title_file_path, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты с некоректным текстовым файлом
            response = self.client.post(reverse(self.url_name), post_context)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверка, что посты не создались
        self.assertEqual(len(list(Post.objects.all())), 0)

        # Отобразилось сообщение об ошибке
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('No posts have been created. Empty post title value'
                                                        ' in line %(line)s') % {'line': 1})

    def test_create_posts_from_file_empty_content(self):
        """Страница создания постов из файла, тест проверющий что посты не создаются если загружается текстовый файл
         c пустым содержанием поста"""
        self._create_test_user_and_login()
        empty_post_content_file_path = os.path.normpath(
            os.path.join(os.getcwd(), 'app_blog/tests/test_files/empty_post_content.txt'))

        with open(empty_post_content_file_path, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты с некоректным текстовым файлом
            response = self.client.post(reverse(self.url_name), post_context)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверка, что посты не создались
        self.assertEqual(len(list(Post.objects.all())), 0)

        # Отобразилось сообщение об ошибке
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('No posts have been created. Empty post'
                                                        ' content value in line %(line)s') % {'line': 1})

    def test_create_posts_from_file_correct_file(self):
        """Страница создания постов из файла, тест проверющий создание постов из корректного файла"""
        self._create_test_user_and_login()
        correct_post_file_path = os.path.normpath(
            os.path.join(os.getcwd(), 'app_blog/tests/test_files/correct_posts_file.txt'))

        with open(correct_post_file_path, 'rb') as file:
            post_context = {'posts_file': file}
            # пытаемся создать посты из корректного файла
            response = self.client.post(reverse(self.url_name), post_context)

        count_lines = get_count_lines_from_file(correct_post_file_path)
        file_lines = get_list_lines_from_file(correct_post_file_path)

        # страница доступна
        self.assertEqual(response.status_code, 200)

        # Проверки, что посты создались
        created_post_list = list(Post.objects.all())
        self.assertEqual(len(created_post_list), count_lines)
        # Собираем информацию из созданных постов в строку в формате загружаемого файла
        posts_in_line_for_check = get_list_lines_in_loading_file_format_from_post_list(created_post_list)
        self.assertEqual(file_lines.sort(), posts_in_line_for_check.sort())

        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('The file was processed successfully. Posted '
                                                        'by %(post_counter)s posts') % {'post_counter': count_lines})
