import csv
from django.core.management.base import BaseCommand
from app.models import Restaurant, Table

class Command(BaseCommand):
    help = "Load restaurants and tables from restaurants.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default="restaurants.csv",
            help="Path to restaurants.csv (default: restaurants.csv in project root)",
        )

    def handle(self, *args, **options):
        path = options["csv"]
        try:
            with open(path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                count_loaded = 0
                for row in reader:
                    name = row.get("restaurant_name", "").strip()
                    location = row.get("location", "").strip()
                    if not name or not location:
                        continue
                    try:
                        size = int(row.get("table_size", "").strip())
                        quantity = int(row.get("table_count", "").strip())
                    except (ValueError, TypeError):
                        continue
                    restaurant, _ = Restaurant.objects.get_or_create(name=name, location=location)
                    table, created = Table.objects.get_or_create(                        restaurant=restaurant,                        size=size,                        defaults={"quantity": quantity},                    )
                    if not created and table.quantity < quantity:
                        table.quantity = quantity
                        table.save()
                    count_loaded += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Done seeding {count_loaded} rows."))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ CSV file not found at {path}"))
