from django.contrib import admin

from apps.shortener.models import ShortUrl


from django.contrib import admin



@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    pass
