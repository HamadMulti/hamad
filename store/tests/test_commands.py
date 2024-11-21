from django.core.management import call_command
from django.test import TestCase
from store.models import Product

class TestSeedDbCommand(TestCase):
    def test_seed_db(self):
        call_command('seed_db_api')
        self.assertTrue(Product.objects.exists())
