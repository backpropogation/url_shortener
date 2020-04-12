import logging

from django.urls import reverse
from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.api.serializers import ShortUrlCreateSerializer, ShortUrlDynamicSerializer
from apps.shortener.models import ShortUrl

logger = logging.getLogger('root')


class ShortUrlViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    parser_classes = (JSONParser,)
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlDynamicSerializer

    def get_session_store(self, request):
        session = request._request.session
        if not session.session_key:
            session.create()
        return session

    def get_queryset(self):
        return self.queryset.filter(session__session_key=self.request._request.session.session_key)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=('redirect_url', 'sub_part'))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=('redirect_url', 'sub_part'))
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        session_store = self.get_session_store(request)
        serializer = ShortUrlCreateSerializer(data=request.data, context={'session_store': session_store})
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.create(serializer.validated_data)
                data = {
                    "redirect_url": serializer.validated_data['redirect_url'],
                    "short_url": request.build_absolute_uri(
                        reverse('redirector', args=(serializer.validated_data['sub_part'],))
                    )
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.info(f'Error on creating subpart')
                logger.exception(e)
                return Response(status=status.HTTP_200_OK, data={'detail': 'gg'})
