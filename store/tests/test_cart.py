from django.test import TestCase
from store.models import Cart, Product, Category

class TestCartModel(TestCase):
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
        self.cart = Cart.objects.create(
            product=self.product,
            quantity=2
        )

    def test_cart_total_price(self):
        self.assertEqual(self.cart.total_price, 599.99 * 2)
