import csv
import os
import random
from A_B_test.test_config import *
from django.core.exceptions import ObjectDoesNotExist
from A_B_test.models import VariantAssignment, Rating


class TestUtils:
    """
    Class to group all test utilities
    """
    __variant = None

    @staticmethod
    def assign_models(users_list):
        """
        Custom function for users randomization between variants
        """
        # Initializing variant counters
        counter = {}
        var_items = variants.copy()
        var_items.popitem()
        for var in var_items.keys():
            counter.update({var: 0})

        # Hashing and sorting users' ids
        hash_ids = []
        for user in users_list:
            hash_ids.append({'hash': hash(str(user.id)), 'user': user})
        random.shuffle(hash_ids)

        # Performing assignment
        for item in hash_ids:
            user = item['user']
            try:
                asg = VariantAssignment.objects.get(user=user.id)
                counter[asg.variant] += 1
            except ObjectDoesNotExist:
                # If user does not have any assignments yet, create it
                var = min(counter, key=counter.get)
                VariantAssignment.objects.create(user=user, variant=var)
                counter[var] += 1
            else:
                pass

    def get_recommendations(self, request):
        if 'variant' in request.session:
            # Getting the assigned model...
            self.__variant = variants[request.session['variant']]
        else:
            # ...or the most popular one
            self.__variant = variants[f'var{len(variants)}']

        recs = self.read_from_tsv(
            os.path.abspath(os.sep.join([recs_manager.output_path, f"{self.__variant.name}.tsv"])),
            request.user.id
        )

        # Getting most popular recommendations for new users (without preferences)
        if not len(recs):
            recs = self.get_most_pop()

        return recs

    @staticmethod
    def read_from_tsv(path, user_id):
        recs = []
        with open(path) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for row in tsv_file:
                if row[0] == str(user_id):
                    recs.append(row[1])
        return recs

    @staticmethod
    def get_most_pop():
        recs = []
        path = os.path.abspath(os.sep.join([recs_manager.output_path, f"MostPop.tsv"]))
        with open(path) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for index, row in zip(range(0, recs_manager.k), tsv_file):
                recs.append(row[1])
        return recs

    def update_ratings(self, request, data):
        recs = self.get_recommendations(request)

        ratings = []
        for r in recs:
            # If request is missing an item from user recs, its rating is set to 0
            item_rating = next((obj for obj in data if obj['item_id'] == r), {'item_id': r, 'rating': 0})
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                item_id=item_rating['item_id'],
                defaults={'rating': item_rating['rating']}
            )
            ratings.append(rating)

        # If user has an assigned variant...
        if 'variant' in request.session:
            # ...store ratings in the .tsv file, too
            self.write_to_tsv(f"data/movies/test_{self.__variant.name}.tsv", ratings)

        return ratings


    @staticmethod
    def write_to_tsv(path, content):
        with open(path, 'a') as file:
            tsv_file = csv.writer(file, delimiter="\t")
            for obj in content:
                tsv_file.writerow([obj.user.id, obj.item_id, obj.rating])
