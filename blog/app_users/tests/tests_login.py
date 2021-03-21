from django.test import TestCase
from django.urls import reverse

from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


class LoginTest(TestCase):
    url_name = 'login'

    def test_login_url_exists_at_desired_location(self):
        """Тест проверки существования страницы login по предпологаемому адресу"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_login_uses_correct_template(self):
        """Тест, проверяющий что страница login использует корректный шаблон"""
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'login.html')

    def test_login(self):
        """Тест проверяющий авторизацию через страницу login"""
        create_test_user()
        context = {'username': TEST_USERNAME, 'password': TEST_USER_PASSWORD}
        response = self.client.post(reverse(self.url_name), context, follow=True)  # важно указать follow=True
        self.assertTrue(response.context['user'].is_authenticated)
        # Проверка перенаправления на страницу постов
        self.assertRedirects(response, expected_url=reverse('post_list'), status_code=302, target_status_code=200)

    def test_login_wrong_user(self):
        """Тест проверяющий невозможность авторизации несуществующего пользователя"""
        context = {'username': 'sfgsdfg', 'password': 'qwerty'}
        response = self.client.post(reverse(self.url_name), context, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_wrong_password(self):
        """Тест проверяющий невозможность авторизации существующего пользователя c неправильным паролем"""
        create_test_user()
        context = {'username': TEST_USERNAME, 'password': f'{TEST_USER_PASSWORD}a'}
        response = self.client.post(reverse(self.url_name), context, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(response.context['user'].is_authenticated)
