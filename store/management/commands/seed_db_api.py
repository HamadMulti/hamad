import requests
from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seed the database with products and categories from an external API"

    def handle(self, *args, **kwargs):
        # API URL
        api_url = "https://fakestoreapi.com/products"

        self.stdout.write("Fetching data from the API...")
        try:
            # Fetch data
            response = requests.get(api_url)
            response.raise_for_status()
            products_data = response.json()

            self.stdout.write("Seeding data into the database...")

            # Add categories and products
            for product_data in products_data:
                category_name = product_data['category']
                category_slug = slugify(category_name)

                # Get or create category
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': category_slug},
                )
                if created:
                    self.stdout.write(f"Category added: {category.name}")

                # Add product
                Product.objects.get_or_create(
                    title=product_data['title'],
                    price=product_data['price'],
                    category=category,
                    description=product_data['description'],
                    image=product_data['image'],
                )
                self.stdout.write(f"Product added: {product_data['title']}")

            self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching data: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
