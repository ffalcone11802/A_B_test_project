import csv
from django.core.management.base import BaseCommand
from A_B_test.models import Rating, User


class Command(BaseCommand):
    """
    Custom command to import ratings into db from .tsv file
    """
    def handle(self, *args, **kwargs):
        tsv_file = 'data/movies/dataset.tsv'

        with open(tsv_file, 'r') as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for row in tsv_file:
                user = User.objects.get(id=row[0])
                Rating.objects.create(
                    user=user,
                    item_id=row[1],
                    rating=row[2]
                )
                self.stdout.write(f"Rating {row} successfully created")
