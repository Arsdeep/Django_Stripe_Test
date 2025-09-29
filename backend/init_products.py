import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_stripe.settings")
django.setup()

from shop.models import Product
Product.objects.all().delete()  # clear old
Product.objects.create(name="Monitor", price=500, description="First product")
Product.objects.create(name="Laptop", price=750, description="Second product")
Product.objects.create(name="Computer", price=900, description="Third product")

print("3 products created successfully!")
