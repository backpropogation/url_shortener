from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path, include
from apps.api.router import router
from django.core.cache import cache

from apps.shortener.models import ShortUrl


def redirect_view(request, sub_part: str):
    redirect_url = cache.get(sub_part, getattr(ShortUrl.objects.filter(sub_part=sub_part).first(), 'sub_part', None))
    if redirect_url:
        return redirect(redirect_url)
    return HttpResponse(status=400)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('<str:sub_part>', redirect_view, name='redirector')

]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
