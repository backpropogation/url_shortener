from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect

from apps.shortener.models import ShortUrl


def redirect_view(request, sub_part: str):
    redirect_url = cache.get(sub_part, getattr(ShortUrl.objects.filter(sub_part=sub_part).first(), 'sub_part', None))
    if redirect_url:
        return redirect(redirect_url)
    return HttpResponse(status=404)
