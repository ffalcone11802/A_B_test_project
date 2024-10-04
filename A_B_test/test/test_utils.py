from django.core.exceptions import ObjectDoesNotExist
from ..models import User, ModelAssignment
from itertools import cycle
from A_B_test_project.config import VARIANTS


def assign_models():
    """
    Custom function for users randomization between models
    """
    users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
    if users:
        for user, model in zip(users, cycle(VARIANTS.keys())):
            obj, created = ModelAssignment.objects.update_or_create(
                user=user,
                defaults={'recommendations_model': model},
            )
    else:
        raise ObjectDoesNotExist
