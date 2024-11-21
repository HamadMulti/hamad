from django.test import TestCase
from store.models import Product, Category


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), self.category.name)


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            title="Smartphone",
            price=599.99,
            category=self.category,
            description="A test smartphone",
            image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwwWL2QLH_sI7YXLh4i1ikDjsRJ7ntiZYRVIH82DcUfbRMbN96rW6DwLrJNZ_GVJ4__tk&usqp=CAU",
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, "Smartphone")
        self.assertEqual(self.product.price, 599.99)
        self.assertEqual(self.product.category.name, "Electronics")
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), self.product.title)
