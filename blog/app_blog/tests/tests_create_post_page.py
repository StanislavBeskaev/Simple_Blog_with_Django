import os
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from app_blog.forms import CreatePostForm
from app_blog.models import Post
from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD, TEST_POSTS_LIST_INFO
from app_media.models import PostImage


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class CreatePostPageTest(TestCase):
    url_name = 'create_post'

    def test_create_post_url_forbidden_with_not_authenticated_user(self):
        """Тест запрета доступа к странице создания постов под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 403)

    def _create_test_user_and_login(self):
        """Метод создаёт тестового пользователя и логиниться под ним"""
        create_test_user()
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)

    def test_create_post_url_exists_at_desired_location_with_authenticated_user(self):
        """Тест доступности страницы создания постов под авторизованным пользователем"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_create_post_uses_correct_template(self):
        """Тест проверяющий, что страница создания постов использует корректный шаблон"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'create_post.html')

    def test_create_post_header_info(self):
        """Тест проверяющий, что в шапке страницы есть необходимая информация"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Welcome to the site'))
        self.assertContains(response, _('To the posts list'))
        self.assertContains(response, _('User information'))
        self.assertContains(response, _('Logout'))

    def test_create_post_form(self):
        """Тест проверяющий форму создания поста"""
        self._create_test_user_and_login()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Create post'))
        self.assertIn(member='form', container=response.context)
        create_post_form = response.context['form']
        self.assertTrue(isinstance(create_post_form, CreatePostForm))

    def test_create_post_without_images(self):
        """Тест создания поста без изображений"""
        self._create_test_user_and_login()
        post_context = {'post_title': TEST_POSTS_LIST_INFO[0]['post_title'],
                        'post_content': TEST_POSTS_LIST_INFO[0]['post_content']}

        response = self.client.post(reverse(self.url_name), post_context)

        # Проверки что создался один пост, с корректным содержимым
        self.assertEqual(len(list(Post.objects.all())), 1)
        created_test_post = Post.objects.filter(post_title=TEST_POSTS_LIST_INFO[0]['post_title']).first()
        self.assertEqual(created_test_post.post_content, TEST_POSTS_LIST_INFO[0]['post_content'])
        post_images_list = list(PostImage.objects.filter(post=created_test_post))
        # Без картинок
        self.assertEqual(len(post_images_list), 0)

        # Проверка перенаправления на страницу списка постов
        self.assertRedirects(response, expected_url=reverse('post_list'), status_code=302,
                             target_status_code=200)

    def test_create_post_wrong_data(self):
        """Тест, что пост не создаётся при передаче пустого содержимого"""
        self._create_test_user_and_login()

        # пытаемся создать пост без названия и содержимого
        response = self.client.post(reverse(self.url_name), {})
        self.assertEqual(response.status_code, 200)

        # форма должна быть не валидной
        create_post_form = response.context['form']
        self.assertFalse(create_post_form.is_valid())

        # Проверка, что пост не создался
        self.assertEqual(len(list(Post.objects.all())), 0)

    def test_create_post_with_images(self):
        """Тест создания поста c изображениями"""
        self._create_test_user_and_login()

        img_1_path = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test_image_1.jpg'))
        img_2_path = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test_image_2.jpg'))
        img_3_path = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test_image_3.jpg'))
        with open(img_1_path, 'rb') as img_1, open(img_2_path, 'rb') as img_2, open(img_3_path, 'rb') as img_3:
            post_context = {'post_title': TEST_POSTS_LIST_INFO[1]['post_title'],
                            'post_content': TEST_POSTS_LIST_INFO[1]['post_content'],
                            'images_field': [img_1, img_2, img_3]
                            }
            response = self.client.post(reverse(self.url_name), post_context)

        # Проверки что создался один пост, с корректным содержимым
        self.assertEqual(len(list(Post.objects.all())), 1)
        created_test_post = Post.objects.filter(post_title=TEST_POSTS_LIST_INFO[1]['post_title']).first()
        self.assertEqual(created_test_post.post_content, TEST_POSTS_LIST_INFO[1]['post_content'])
        # и тремя изображениями
        post_images_list = list(PostImage.objects.filter(post=created_test_post))
        self.assertEqual(len(post_images_list), 3)

        # Проверка перенаправления на страницу списка постов
        self.assertRedirects(response, expected_url=reverse('post_list'), status_code=302,
                             target_status_code=200)

    def test_create_post_with_wrong_file(self):
        """Тест, что пост не создаётся если вместо картинки передать текстовый файл"""
        self._create_test_user_and_login()

        img_1_path = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test_image_1.jpg'))
        bad_file_path = os.path.normpath(os.path.join(os.getcwd(), 'app_blog/tests/test_files/test.txt'))

        with open(img_1_path, 'rb') as img_1, open(bad_file_path, 'rb') as bad_file:
            post_context = {'post_title': TEST_POSTS_LIST_INFO[1]['post_title'],
                            'post_content': TEST_POSTS_LIST_INFO[1]['post_content'],
                            'images_field': [img_1, bad_file]
                            }
            # пытаемся создать пост с приложенным текстовым файлом
            response = self.client.post(reverse(self.url_name), post_context)

        # форма должна быть не валидной
        create_post_form = response.context['form']
        self.assertFalse(create_post_form.is_valid())

        # Проверка, что пост не создался
        self.assertEqual(len(list(Post.objects.all())), 0)
