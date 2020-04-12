from rest_framework.routers import DefaultRouter

from apps.api.viewsets import ShortUrlViewSet

router = DefaultRouter()
router.register('shorturls', ShortUrlViewSet, basename='shorturls')
