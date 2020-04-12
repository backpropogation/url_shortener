from django.contrib.sessions.models import Session
from django.db import models


class ShortUrl(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name='Session'
    )
    redirect_url = models.URLField()
    sub_part = models.CharField(
        max_length=8,
        verbose_name='Sub part'
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.redirect_url}'

    class Meta:
        indexes = (
            models.Index(fields=('sub_part',)),
            models.Index(fields=('redirect_url',)),
        )