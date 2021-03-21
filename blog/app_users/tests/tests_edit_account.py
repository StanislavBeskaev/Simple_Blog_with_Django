from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from app_users.forms import UserAccountEditForm
from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


class EditAccountTest(TestCase):
    url_name = 'edit_account'

    def setUpTestData():
        """Для всех тестов создаётся тестовый пользователь"""
        create_test_user()

    def test_edit_account_url_forbidden_with_not_authenticated_user(self):
        """Тест запрета доступа к странице редактирование данных пользователя под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 403)

    def test_edit_account_url_exists_at_desired_location(self):
        """Тест проверки существования страницы редактирование данных пользователя по предпологаемому адресу под
         авторизованным пользователем"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_edit_account_uses_correct_template(self):
        """Тест проверяющий, что страница редактирования данных пользователя использует корректный шаблон"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'edit_account.html')

    def test_edit_account_form(self):
        """Тест проверяющий используемую форму на странице редактирования данных пользователя"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        # На странице есть форма и она верная
        self.assertIn(member='edit_form', container=response.context)
        self.assertTrue(isinstance(response.context['edit_form'], UserAccountEditForm))

    def test_edit_account(self):
        """Тест проверяющий изменение данных пользователя через страницу изменения данных пользователя"""
        new_email = 'new_email@test.com'
        new_first_name = 'new first name'
        new_last_name = 'new last name'
        context = {'email': new_email, 'first_name': new_first_name, 'last_name': new_last_name}

        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse(self.url_name), context)

        # Форма валидна
        self.assertTrue(response.context['edit_form'].is_valid())
        self.assertIn(member='message', container=response.context)
        self.assertContains(response, _('Changes saved!'))

        updated_user = User.objects.filter(username=TEST_USERNAME).first()

        # Проверки, что данные пользователя обновлены
        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(updated_user.first_name, new_first_name)
        self.assertEqual(updated_user.last_name, new_last_name)

    def test_edit_account_wrong_email(self):
        """Тест проверяющий, что данные пользователя не изменяются если ввести неправильный email"""
        wrong_email = 'new_email@test'
        new_first_name = 'new first name'
        new_last_name = 'new last name'
        bad_context = {'email': wrong_email, 'first_name': new_first_name, 'last_name': new_last_name}

        current_user = User.objects.filter(username=TEST_USERNAME).first()
        old_email = current_user.email
        old_first_name = current_user.first_name
        old_last_name = current_user.last_name

        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        # Пробуем изменить данные при неправильном email
        response = self.client.post(reverse(self.url_name), bad_context)

        # Форма не валидна
        self.assertFalse(response.context['edit_form'].is_valid())
        self.assertIn(member='message', container=response.context)
        self.assertContains(response, _('Please enter correct data'))

        # Проверки, что данные пользователя не изменились
        user = User.objects.filter(username=TEST_USERNAME).first()
        self.assertEqual(user.email, old_email)
        self.assertEqual(user.first_name, old_first_name)
        self.assertEqual(user.last_name, old_last_name)
