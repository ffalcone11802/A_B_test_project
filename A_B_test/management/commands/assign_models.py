from django.core.management.base import BaseCommand
from A_B_test.models import User
from A_B_test.test.test_utils import assign_models


class Command(BaseCommand):
    """
    Custom command to assign models to users
    """
    def handle(self, *args, **kwargs):
        users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
        if users:
            assign_models(users)
            self.stdout.write(f'Assignment successfully performed')
        else:
            self.stdout.write(f'Failed to perform assignment: no users found')
