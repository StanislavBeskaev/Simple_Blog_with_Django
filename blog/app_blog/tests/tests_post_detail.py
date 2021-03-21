import datetime
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from core.test_handlers import TEST_USERNAME, TEST_USER_PASSWORD, create_test_posts, \
    TEST_POSTS_LIST_INFO, PUBLICATION_DATETIME_FORMAT


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostDetailTest(TestCase):
    url_name = 'post_detail'

    def setUpTestData():
        """Метод предварительных действий. Перед запуском тестов создаём тестовые посты"""
        create_test_posts()  # в этом методе создаётся тестовый пользователь TEST_USERNAME/ TEST_USER_PASSWORD

    def _login_test_user(self):
        """Метод создаёт тестового пользователя и логиниться под ним"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)

    def test_post_detail_url_exists_at_desired_location(self):
        """Тест доступности страниц детальной информации о посте"""
        # Проверяем, что доступны все страницы созданных постов
        for i in range(len(TEST_POSTS_LIST_INFO)):
            response = self.client.get(reverse(self.url_name, kwargs={'pk': i+1}))
            self.assertEqual(response.status_code, 200)

    def test_post_detail_uses_correct_template(self):
        """Тест, проверяющий что страница детальной информации о посте использует корректный шаблон"""
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_detail_header_with_not_authenticated_user(self):
        """Тест проверяющий информацию в шапке страницы под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 1}))
        self.assertContains(response, _('You are logged in as an unauthorized user'))
        self.assertContains(response, _('To the posts list'))
        self.assertContains(response, _('Login'))
        self.assertNotContains(response, _('Welcome to the site'))
        self.assertNotContains(response, _('User information'))

    def test_post_detail_header_with_authenticated_user(self):
        """Тест проверяющий информацию в шапке страницы под авторизованным пользователем"""
        self._login_test_user()
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, _('You are logged in as an unauthorized user'))
        self.assertContains(response, _('To the posts list'))
        self.assertNotContains(response, _('Login'))
        self.assertContains(response, _('Welcome to the site'))
        self.assertContains(response, _('User information'))
        self.assertContains(response, _('Logout'))

    def test_post_detail_content(self):
        """Тест проверяющий содержимое страниц детальной информации о посте"""
        for index, post_info in enumerate(TEST_POSTS_LIST_INFO):
            response = self.client.get(reverse(self.url_name, kwargs={'pk': index+1}))
            self.assertContains(response, post_info['post_title'])
            self.assertContains(response, post_info['post_content'])
            self.assertContains(response, TEST_USERNAME)
            publication_date = datetime.datetime.strptime(post_info['publication_date'], PUBLICATION_DATETIME_FORMAT)
            self.assertContains(response, publication_date.strftime('%Y-%m-%d %H:%M:%S'))
