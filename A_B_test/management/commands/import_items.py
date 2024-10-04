import csv
from django.core.management.base import BaseCommand
from A_B_test.models import Item


class Command(BaseCommand):
    """
    Custom command to import items into db from .csv file
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['title']
                # If items does not already exist...
                if not Item.objects.filter(title=title).exists():
                    score = row['score'] if row['score'] else 0
                    # ... create it
                    Item.objects.create(
                        title=title,
                        description=row['description'],
                        score=score
                    )
                    self.stdout.write(f"Item {title} successfully created")
                else:
                    self.stdout.write(f"Item {title} already exists")
