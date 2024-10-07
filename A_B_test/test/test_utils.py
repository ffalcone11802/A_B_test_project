from ..models import ModelAssignment
from itertools import cycle
from A_B_test_project.config import VARIANTS


def assign_models(users_list):
    """
    Custom function for users randomization between models
    """
    users_id = users_list.values_list('id', flat=True)

    # Hashing users id and sorting them
    hashed_id = [hash(str(user_id)) for user_id in users_id]
    hash_user_id = sorted(zip(hashed_id, users_id))

    for id_hash, model in zip(hash_user_id, cycle(VARIANTS.keys())):
        user = next((x for x in users_list if x.id == id_hash[1]), None)
        obj, created = ModelAssignment.objects.update_or_create(
            user=user,
            defaults={'recommendations_model': model},
        )
