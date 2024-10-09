import pandas as pd
from django.core.management.base import BaseCommand
from A_B_test.models import Item
from A_B_test_project.config import DataSet


class Command(BaseCommand):
    """
    Custom command to import items into db from .csv file
    """
    def handle(self, *args, **kwargs):
        csv_file = DataSet.ITEMS.value

        with open(csv_file, 'r') as file:
            items = pd.read_csv(file)

            # Set item score to 0 if not present
            items.fillna({'score': 0}, inplace=True)

            for row in items.iterrows():
                title = row[1]['title']
                description = row[1]['description']
                score = row[1]['score']
                # If items does not already exist...
                if not Item.objects.filter(title=title).exists():
                    # ... create it
                    Item.objects.create(
                        title=title,
                        description=description,
                        score=score
                    )
                    self.stdout.write(f"Item {title} successfully created")
                else:
                    self.stdout.write(f"Item {title} already exists")
