from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.shortener.models import ShortUrl


@receiver(post_save, sender=ShortUrl)
def on_create_short_url(sender, instance, created, **kwargs):
    if created:
        cache.set(f'{instance.sub_part}', instance.redirect_url, timeout=settings.URL_TIMEOUT)


@receiver(pre_delete, sender=ShortUrl)
def on_delete_short_url(sender, instance, **kwargs):
    cache.delete(f'{instance.sub_part}')
