import requests
import json
from django.core.management.base import BaseCommand
from peru_api.models import Category
from django.conf import settings
import requests
import json


class Command(BaseCommand):
    help = "Categories write"

    def handle(self, *args, **options):
        r = requests.get("https://iptv-org.github.io/api/categories.json")

        with open(settings.DATA_DIR / "categories.json", "w+") as f:
            data = json.dumps(r.json())
            f.write(data)
        with open(settings.DATA_DIR / "categories.json", "r") as f:
            category_objects = []
            data = json.loads(f.read())
            for item in data:
                category_object = Category(
                    category_id=item["id"], category_name=item["name"]
                )
                category_objects.append(category_object)
            Category.objects.bulk_create(category_objects)
