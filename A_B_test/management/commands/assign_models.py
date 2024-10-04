from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from A_B_test.test.test_utils import assign_models


class Command(BaseCommand):
    """
    Custom command to assign models to users
    """
    def handle(self, *args, **kwargs):
        try:
            assign_models()
        except ObjectDoesNotExist:
            self.stdout.write(f'Failed to perform assignment: no users found')
        else:
            self.stdout.write(f'Assignment successfully performed')
