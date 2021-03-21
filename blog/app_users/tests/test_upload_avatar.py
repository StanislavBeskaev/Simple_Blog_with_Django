import os
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from app_users.models import Profile
from core.test_handlers import create_test_user, TEST_USERNAME, TEST_USER_PASSWORD


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class UploadAvatarTest(TestCase):
    url_name = 'upload_avatar'

    def setUpTestData():
        """Для всех тестов создаётся тестовый пользователь"""
        create_test_user()

    def test_upload_avatar_url_forbidden_with_not_authenticated_user(self):
        """Тест проверки запрета доступа к странце загрузки аватарки под неавторизованным пользователем"""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 403)

    def test_upload_avatar_url_exists_at_desired_location_with_authenticated_user(self):
        """Тест проверки доступности страницы загрузки аватарки под авторизованным пользователем"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_upload_avatar_uses_correct_template(self):
        """Тест проверки, что страница загрузки аватарки использует корректный шаблон"""
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'upload_avatar.html')

    def test_upload_avatar(self):
        """Тест работоспособности загрузки аватарки через страницу загрузки аватарки"""
        img_path = os.path.normpath(os.path.join(os.getcwd(), 'app_users/tests/test_files/test_image_1.jpg'))

        user_profile = Profile.objects.filter(user__username=TEST_USERNAME).first()
        # Проверка, что у пользователя не было аватарки
        self.assertIsNone(user_profile.avatar_image_file)

        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        with open(img_path, 'rb') as img_1:
            context = {'avatar_image_file': img_1}
            response = self.client.post(reverse(self.url_name), context)

        self.assertRedirects(response, expected_url=reverse('account'), status_code=302, target_status_code=200)
        updated_user_profile = Profile.objects.filter(user__username=TEST_USERNAME).first()
        # Проверка, что у пользователя не пустая аватарка
        self.assertIsNotNone(updated_user_profile.avatar_image_file)

    def test_upload_avatar_with_wrong_file(self):
        """Тест проверяющий, что аватарка не загружается, если указать текстовый файл"""
        txt_path = os.path.normpath(os.path.join(os.getcwd(), 'app_users/tests/test_files/test.txt'))

        user_profile = Profile.objects.filter(user__username=TEST_USERNAME).first()
        # Проверка, что у пользователя не было аватарки
        self.assertIsNone(user_profile.avatar_image_file)
        self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        with open(txt_path, 'rb') as bad_file:
            context = {'avatar_image_file': bad_file}
            # Пытаемся загрузить текстовый файл вместо картинки
            response = self.client.post(reverse(self.url_name), context)

        self.assertEqual(response.status_code, 200)
        self.assertIn(member='edit_form', container=response.context)

        # Форма загрузки не валидна
        self.assertFalse(response.context['edit_form'].is_valid())
        self.assertIn(member='message', container=response.context)
        self.assertEqual(response.context['message'], _('Specify the correct file'))

        updated_user_profile = Profile.objects.filter(user__username=TEST_USERNAME).first()
        # Проверка, что у пользователя не появилось аватарки
        self.assertIsNone(updated_user_profile.avatar_image_file)
