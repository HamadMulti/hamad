from django.test import TestCase
from django.urls import reverse
from store.models import Product, Category

class TestHomeView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Smartphone",
            price=599.99,
            category=self.category,
            description="A test smartphone",
            image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwwWL2QLH_sI7YXLh4i1ikDjsRJ7ntiZYRVIH82DcUfbRMbN96rW6DwLrJNZ_GVJ4__tk&usqp=CAU",
            stock=10
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')
        self.assertContains(response, "Smartphone")

class TestProductDetailView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Smartphone",
            price=599.99,
            category=self.category,
            description="A test smartphone",
            image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwwWL2QLH_sI7YXLh4i1ikDjsRJ7ntiZYRVIH82DcUfbRMbN96rW6DwLrJNZ_GVJ4__tk&usqp=CAU",
            stock=10
        )

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertContains(response, "Smartphone")
