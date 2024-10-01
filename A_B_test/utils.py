from models import User, ModelAssignment
from itertools import cycle
from A_B_test_project.config import models


def assign_models():
    """
    Custom function for users randomization between models
    """
    users_id = User.objects.values_list('id')
    hashed_id = [hash(str(user_id)) for user_id in users_id]
    hashed_id.sort()
    hashed_id.reverse()

    for hashed_user_id, model in zip(hashed_id, cycle(models.keys())):
        obj, created = ModelAssignment.objects.update_or_create(
            hashed_user_id=hashed_user_id,
            defaults={'recommendations_model': model},
        )


def clear_assignments():
    """
    Custom function to clear users randomization
    """
    hashed_users_id = ModelAssignment.objects.values_list('id')
    for hashed_user_id in hashed_users_id:
        assignment = ModelAssignment.objects.get(hashed_user_id=hashed_user_id)
        assignment.recommendations_model = None
        assignment.save()
