from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


class LogoutTest(TestCase):
    url_name = 'logout'

    def test_logout_url_exists_at_desired_location(self):
        """Тест проверки существования страницы logout по предпологаемому адресу"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Тест проверки выхода из системы"""
        create_test_user()
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('You are logged out'))
        self.assertContains(response, _('To the posts list'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_uses_correct_templates(self):
        """Тест, проверяющий что страница logout испльзует корректный шаблон"""
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'logout.html')
