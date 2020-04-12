from datetime import timedelta

from django.utils.timezone import now

from apps.shortener.models import ShortUrl


def _clear_expired_links():
    qs = ShortUrl.objects.filter(created_at__lte=now() - timedelta(minutes=15))
    qs.delete()
