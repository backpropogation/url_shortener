from django.urls import reverse
from factory.fuzzy import FuzzyText
from faker import Faker
from rest_framework.test import APITestCase


class ShortUrlTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.urls_count = 10

    def test_get_list_of_urls_without_creation(self):
        url = reverse('shorturls-list')
        response = self.client.get(url)
        self.assertEqual(response.data, [])

    def test_create_urls(self):
        url = reverse('shorturls-list')
        for _ in range(self.urls_count):
            sub_part = FuzzyText(length=8).fuzz()
            data = {
                "redirect_url": self.fake.url(),
                "sub_part": sub_part
            }
            response = self.client.post(url, data=data, format='json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(sub_part in response.data.get('short_url'))

    def test_create_urls_and_get_them(self):
        url = reverse('shorturls-list')
        for _ in range(self.urls_count):
            sub_part = FuzzyText(length=8).fuzz()
            data = {
                "redirect_url": self.fake.url(),
                "sub_part": sub_part
            }
            self.client.post(url, data=data, format='json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.urls_count)

    def test_get_list_of_urls_of_other_session(self):
        url = reverse('shorturls-list')
        sub_part = FuzzyText(length=8).fuzz()
        data = {
            "redirect_url": self.fake.url(),
            "sub_part": sub_part
        }
        self.client.post(url, data=data, format='json')
        response = self.client.get(url)

        # Ensure that this session has associated short urls
        self.assertEqual(len(response.data), 1)
        self.client.cookies.clear()

        # Ensure that another session short urls aren't available
        response = self.client.get(url)
        self.assertEqual(response.data, [])
