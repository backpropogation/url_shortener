from django.core.validators import RegexValidator
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.shortener.utils.generate_sub_part import generate_sub_part
from apps.shortener.models import ShortUrl


class ShortUrlDynamicSerializer(serializers.ModelSerializer):
    sub_part = serializers.SerializerMethodField()

    class Meta:
        model = ShortUrl
        fields = ('redirect_url', 'sub_part')

    def get_sub_part(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(reverse('redirector', args=(obj.sub_part,)))

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(ShortUrlDynamicSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ShortUrlCreateSerializer(serializers.ModelSerializer):
    sub_part = serializers.CharField(required=False, max_length=8)

    class Meta:
        model = ShortUrl
        fields = ('redirect_url', 'sub_part')

    # noinspection PyMethodMayBeStatic
    def validate_sub_part(self, sub_part):
        RegexValidator(regex='^[a-zA-Z0-9]*$', message='Enter valid sub part')(sub_part)
        if ShortUrl.objects.filter(sub_part=sub_part).exists():
            raise ValidationError('Already exists.')
        else:
            return sub_part

    def create(self, validated_data):
        if 'sub_part' not in validated_data:
            validated_data['sub_part'] = generate_sub_part()
        # noinspection PyProtectedMember
        session = self.context['session_store']._get_session_from_db()
        obj = ShortUrl.objects.create(**validated_data, session=session)
        return obj

    def to_representation(self, instance_dict):
        return {
            "redirect_url": instance_dict['redirect_url'],
            "short_url": self.context['request'].build_absolute_uri(
                reverse('redirector', args=(instance_dict['sub_part'],))
            )
        }
