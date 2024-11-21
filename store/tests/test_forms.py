from django.test import TestCase
from store.forms import CustomForm

class TestCustomForm(TestCase):
    def test_form_valid_data(self):
        form = CustomForm(data={"field1": "value1", "field2": "value2"})
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = CustomForm(data={"field1": "", "field2": "value2"})
        self.assertFalse(form.is_valid())
