import re
from urllib.parse import urlparse
from rest_framework.serializers import ValidationError


class ExternalLinksValidator:
    """Класс для валидации содержимого текстового поля, в котором проходит проверка на присутствие сторонних ссылок
    и запрета на них, кроме ссылки на 'youtube.com'"""

    def __init__(self, field):
        """Конструктор класса ExternalLinksValidator"""

        self.field = field

    def __call__(self, value):
        """Вызываемый метод для проверки наличия ссылок в тексте поля"""

        # Проверка на принимаемый формат данных (если значение не словарь, вызывается ошибка)
        if not isinstance(value, dict):
            raise ValidationError("Некорректный формат данных")

        # Получаем переменную text по значению ключа и проверяем что text это str и не None
        text = value.get(self.field)
        if not text or not isinstance(text, str):
            return 'Поле пустое или не строка'

        # Проверяем, содержит ли текст URL, ищем все ссылки в text
        urls = re.findall(r'https?://[^\s)\]]+', text)
        # С помощью urlparse, разбиваем ссылку на компоненты и забираем сетевую локацию netloc
        for url in urls:
            parsed = urlparse(url)
            netloc = parsed.netloc.lower()
            # Разрешаем только YouTube-ссылки
            if not any(
                domain in netloc
                for domain in ("youtube.com", "youtu.be", "www.youtube.com", "m.youtube.com")
            ):
                raise ValidationError(
                    "Запрещено использовать сторонние ссылки, кроме YouTube."
                )
