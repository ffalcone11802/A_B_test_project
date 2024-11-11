from django.core.management.base import BaseCommand
from A_B_test.models import User
import random
random.seed(36)

class Command(BaseCommand):
    """
    Custom command to import users into db from .csv file
    """
    def handle(self, *args, **kwargs):
        file = 'datasets/Nuovo Documento di testo.txt'
        lines = open(file).read().splitlines()
        # users = User.objects.all()

        # for u in users:
        u = User.objects.get(id=26)
        for _ in range(0, 60):
            my_line = random.choice(lines)
            u.preferences.append(my_line)

        u.save()
        print(f'Preferences for user {u.username} successfully updated ')
