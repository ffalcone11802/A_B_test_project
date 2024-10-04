import csv
from django.core.management.base import BaseCommand
from A_B_test.models import User


class Command(BaseCommand):
    """
    Custom command to import users into db from .csv file
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['username']
                # If user does not already exist...
                if not User.objects.filter(username=username).exists():
                    # ... create it
                    User.objects.create_user(
                        username=username,
                        email=row['email'],
                        password=row['password'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                    self.stdout.write(f"User {username} successfully created")
                else:
                    self.stdout.write(f"User {username} already exists")
