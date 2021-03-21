from django.test import TestCase
from django.urls import reverse


from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_FIRST_NAME, TEST_USER_LAST_NAME, \
    TEST_USER_EMAIL, TEST_USER_PASSWORD


class AccountTest(TestCase):
    url_name = 'account'

    def setUpTestData():
        """Для всех тестов создаётся тестовый пользователь"""
        create_test_user()

    def test_account_url_forbidden_with_not_authenticated_user(self):
        """Тест запрета доступа к странице информации о пользователе под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 403)

    def test_account_url_exists_at_desired_location(self):
        """Тест проверки существования страницы информации о пользователе по предпологаемому адресу под
         авторизованным пользователем"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_account_uses_correct_template(self):
        """Тест, проверяющий что страница информации о пользователе использует корректный шаблон"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'account.html')

    def test_account_content(self):
        """Тест проверки содержимого страницы информации о пользователе"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, TEST_USERNAME)
        self.assertContains(response, TEST_USER_FIRST_NAME)
        self.assertContains(response, TEST_USER_LAST_NAME)
        self.assertContains(response, TEST_USER_EMAIL)
