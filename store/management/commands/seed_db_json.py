import json
import random
import os
from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify
from django.conf import settings

class Command(BaseCommand):
    help = "Seed the database with products and categories from a local JSON file"

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'products.json')

        # Ensure the file exists
        if not os.path.exists(json_file_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {json_file_path}"))
            return

        self.stdout.write(f"Reading data from {json_file_path}...")
        try:
            # Open and load data from JSON file
            with open(json_file_path, 'r') as f:
                products_data = json.load(f)

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

                # Generate random stock
                random_stock = random.randint(1, 100)  # Stock between 1 and 100

                # Add product
                Product.objects.get_or_create(
                    title=product_data['title'],
                    price=product_data['price'],
                    category=category,
                    description=product_data['description'],
                    image=product_data['image'],
                    stock=random_stock,  # Assign random stock
                )
                self.stdout.write(f"Product added: {product_data['title']} with stock {random_stock}")

            self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Error reading the JSON file: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
