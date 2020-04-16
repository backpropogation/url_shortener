from django.urls import reverse


def build_redirect_url(request, sub_part):
    return request.build_absolute_uri(reverse('redirector', args=(sub_part,)))
