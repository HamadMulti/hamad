import json
import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Fetch products from an API and save them to a JSON file"

    def handle(self, *args, **kwargs):
        # API URL
        api_url = "https://fakestoreapi.com/products"

        self.stdout.write("Fetching products from the API...")
        try:
            # Fetch products
            response = requests.get(api_url)
            response.raise_for_status()
            products = response.json()

            # Define output file path
            output_dir = os.path.join(settings.BASE_DIR, 'data')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, 'products.json')

            # Write products to JSON file
            with open(output_file, 'w') as file:
                json.dump(products, file, indent=4)

            self.stdout.write(self.style.SUCCESS(f"Products saved to {output_file}"))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching products: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
