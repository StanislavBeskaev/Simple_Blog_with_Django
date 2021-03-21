import datetime
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from app_blog.services.post_services import SHORT_CONTENT_LENGTH
from core.test_handlers import create_test_posts, TEST_POSTS_LIST_INFO, PUBLICATION_DATETIME_FORMAT, \
    create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostListTest(TestCase):
    url_name = 'post_list'

    def test_post_list_url_exists_at_desired_location(self):
        """Тест проверки существования страницы постов по предпологаемому адресу"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_post_list_uses_correct_template(self):
        """Тест проверяющий, что страница постов использует корректный шаблон"""
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'post_list.html')

    def test_post_list_without_posts(self):
        """Тест проверяющий содержимое страницы списка постов без наличия постов"""
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('There are no posts'))

    def test_post_list_with_posts_content(self):
        """Тест проверяющий содержимое страницы списка постов при наличии постов"""
        create_test_posts()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Blog posts list'))
        self.assertIn(member='post_list', container=response.context)
        self.assertEqual(len(response.context['post_list']), len(TEST_POSTS_LIST_INFO))
        for post_info in TEST_POSTS_LIST_INFO:
            self.assertContains(response, post_info['post_title'])
            self.assertContains(response, post_info['post_content'][:SHORT_CONTENT_LENGTH])
            publication_date = datetime.datetime.strptime(post_info['publication_date'], PUBLICATION_DATETIME_FORMAT)
            self.assertContains(response, publication_date.strftime('%Y-%m-%d'))

    def test_post_list_ordering(self):
        """Тест проверяющий уборядочены ли посты на страницы списка постов по дате публикации в порядке убывания"""
        create_test_posts()
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('Blog posts list'))
        self.assertIn(member='post_list', container=response.context)
        previous_post = response.context['post_list'][0]
        for post in response.context['post_list']:
            self.assertGreaterEqual(previous_post.publication_date, post.publication_date)
            previous_post = post

    def test_post_list_header_with_not_authenticated_user(self):
        """Тест проверяющий шапку страницы списка постов при доступе не авторизованного пользователя"""
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, _('You are logged in as an unauthorized user'))
        self.assertContains(response, _('Login'))
        self.assertNotContains(response, _('Welcome to the site'))
        self.assertNotContains(response, _('User information'))
        self.assertNotContains(response, _('Create post'))
        self.assertNotContains(response, _('Creating posts from a file'))
        self.assertNotContains(response, _('Logout'))

    def test_post_list_header_with_authenticated_user(self):
        """Тест проверяющий шапку страницы списка постов при доступе авторизованного пользователя"""
        create_test_user()
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertNotContains(response, _('You are logged in as an unauthorized user'))
        self.assertNotContains(response, _('Login'))
        self.assertContains(response, _('Welcome to the site'))
        self.assertContains(response, _('User information'))
        self.assertContains(response, _('Create post'))
        self.assertContains(response, _('Creating posts from a file'))
        self.assertContains(response, _('Logout'))
