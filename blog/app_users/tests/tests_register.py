from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


class RegisterTest(TestCase):
    url_name = 'register'

    def setUpTestData():
        """Для всех тестов создаётся тестовый пользователь"""
        create_test_user()

    def test_register_url_exists_at_desired_location(self):
        """Тест проверки существования страницы регистрации по предпологаемому адресу"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_register_uses_correct_template(self):
        """Тест, проверяющий что страница login использует корректный шаблон"""
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'register.html')

    def test_register_same_user(self):
        """Тест проверки ошибки при регистрации уже существующего пользователя"""
        context = {'username': TEST_USERNAME, 'password1': TEST_USER_PASSWORD, 'password2': TEST_USER_PASSWORD}
        response = self.client.post(reverse(self.url_name), context)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_register(self):
        """Тест проверки регистрации нового пользователя"""
        new_username = f'{TEST_USERNAME}1'
        new_password = 'c0olP@sw'
        first_name = 'new firsts name'
        last_name = 'new last name'
        email = 'new_test@test.com'
        context = {'username': new_username,
                   'password1': new_password,
                   'password2': new_password,
                   'first_name': first_name,
                   'last_name': last_name,
                   'email': email}
        response = self.client.post(reverse(self.url_name), context, follow=True)

        # Проверки, что создался пользователь с нужными данными
        new_user = User.objects.filter(username=new_username).first()
        self.assertEqual(new_user.first_name, first_name)
        self.assertEqual(new_user.last_name, last_name)
        self.assertEqual(new_user.email, email)

        self.assertTrue(response.context['user'].is_authenticated)
        # Проверка перенаправления на страницу постов
        self.assertRedirects(response, expected_url=reverse('post_list'), status_code=302, target_status_code=200)

    def test_register_error(self):
        """Тест проверки ошибки при регистрации при вводе простых паролей"""
        context = {'username': 'test_user_name', 'password1': '1234', 'password2': '1234'}
        response = self.client.post(reverse(self.url_name), context)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
