import pandas as pd
from django.core.management.base import BaseCommand
from A_B_test.models import User
from A_B_test_project.config import DataSet


class Command(BaseCommand):
    """
    Custom command to import users into db from .csv file
    """
    def handle(self, *args, **kwargs):
        csv_file = DataSet.USERS.value

        with open(csv_file, 'r') as file:
            users = pd.read_csv(file)

            for row in users.iterrows():
                username = row[1]['username']
                # If user does not already exist...
                if not User.objects.filter(username=username).exists():
                    # ... create it
                    User.objects.create_user(
                        username=username,
                        email=row[1]['email'],
                        password=row[1]['password'],
                        first_name=row[1]['first_name'],
                        last_name=row[1]['last_name']
                    )
                    self.stdout.write(f"User {username} successfully created")
                else:
                    self.stdout.write(f"User {username} already exists")
