import secrets

from apps.shortener.models import ShortUrl
from apps.shortener.utils import NoAvailableSubPartException


def generate_sub_part():
    for _ in range(100):
        sub_part = secrets.token_urlsafe(6)
        if ShortUrl.objects.filter(sub_part=sub_part).exists():
            continue
        return sub_part
    raise NoAvailableSubPartException("No  subpart  is available.")
