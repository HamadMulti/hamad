import requests
from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify
import random
import os


class Command(BaseCommand):
    help = "Seed the database with products and categories from an external API"

    def handle(self, *args, **kwargs):
        api_url = "https://fakestoreapi.com/products"

        self.stdout.write("Fetching data from the API...")
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            products_data = response.json()

            self.stdout.write("Seeding data into the database...")

            for product_data in products_data:
                category_name = product_data.get('category', 'Uncategorized')
                category_slug = slugify(category_name)

                # Create category if not exists
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': category_slug},
                )
                if created:
                    self.stdout.write(f"Category created: {category.name}")

                # Handle missing data
                title = product_data.get(
                    'title', f"Product-{random.randint(1000, 9999)}")
                price = product_data.get(
                    'price', round(random.uniform(10, 500), 2))
                description = product_data.get(
                    'description', 'No description available.')
                image = product_data.get('image', 'placeholder.jpg')
                stock = random.randint(1, 100)

                # Check or create product
                product, created = Product.objects.get_or_create(
                    title=title,
                    defaults={
                        'price': price,
                        'category': category,
                        'description': description,
                        'image': image,
                        'stock': stock,
                        'slug': slugify(title),
                        'sku': f"SKU-{random.randint(1000, 9999)}",
                    },
                )
                if created:
                    self.stdout.write(f"Product added: {title}")
                else:
                    self.stdout.write(f"Product already exists: {title}")

            self.stdout.write(self.style.SUCCESS(
                "Database seeding completed!"))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching data: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
