import re
from urllib.parse import urlparse

from rest_framework import serializers


class VideoUrlValidator:
    """Проверка содержания материалов на наличие сторонних ссылок"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*'
        for item in self.field:
            temp_value = dict(value).get(item)
            if temp_value:
                urls = re.findall(url_pattern, temp_value)

                for url in urls:
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.lower()

                    # Разрешаем только YouTube
                    allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be']

                    if not any(allowed_domain in domain for allowed_domain in allowed_domains):
                        raise serializers.ValidationError("Разрешены только ссылки на YouTube")
