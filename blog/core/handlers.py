"""Модуль с общими функциями"""
import os

from blog.settings import MEDIA_URL


def get_correct_file_path_to_img_tag(file_field) -> str:
    """Метод возращает корректный путь до файла для src тега <img>"""
    return os.path.join(MEDIA_URL, str(file_field))
