from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import home, product_detail

class TestUrls(SimpleTestCase):
    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_product_detail_url(self):
        url = reverse('product_detail', args=['smartphone'])
        self.assertEqual(resolve(url).func, product_detail)
