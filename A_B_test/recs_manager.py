import importlib
import os
from A_B_test.models import Rating
from elliot.namespace.namespace_model_builder import NameSpaceBuilder
from elliot.utils.write import store_recommendation
import A_B_test.test_config as config

here = os.path.abspath(os.path.dirname(__file__))


class RecsManager:
    def __init__(self, config_path):
        self.__builder = NameSpaceBuilder(config_path, here, os.path.abspath(os.path.dirname(config_path)))
        self.__base = self.__builder.base
        self.output_path = self.__base.base_namespace.path_output_rec_result
        self.k = self.__base.base_namespace.top_k

    def update_recs(self):
        self.__write_tsv()
        self.__train_models_and_compute_recs()

    @staticmethod
    def __write_tsv():
        print("Reading ratings from db ...")
        ratings = Rating.objects.all()
        tsv_ratings = []

        for r in ratings:
            tsv_ratings.append(str(r.user.id)+'\t'+str(r.item_id)+'\t'+str(r.rating)+'\n')

        print("Printing ratings to data/movies/ ...")
        os.makedirs("data/movies", exist_ok=True)
        with open("data/movies/dataset.tsv", "w") as f:
            f.writelines(tsv_ratings)

    def __train_models_and_compute_recs(self):
        print("Training models ...")
        dataloader_class = getattr(importlib.import_module("elliot.dataset"), self.__base.base_namespace.data_config.dataloader)
        dataloader = dataloader_class(config=self.__base.base_namespace)
        data_test_list = dataloader.generate_dataobjects()
        count = 0

        for key, model_base in self.__builder.models():
            count += 1
            for test_fold_index, data_test in enumerate(data_test_list):
                model_class = getattr(importlib.import_module("elliot.recommender"), key)
                for data_obj in data_test:
                    model = model_class(data=data_obj, config=self.__base.base_namespace, params=model_base)
                    model.train()
                    self.__compute_recommendations(model)
                    config.variants.update({f'var{count}': model})

    def __compute_recommendations(self, model):
        recs = model.get_recommendations(self.k)
        if model._save_recs:
            print(f"Writing recommendations at: {self.output_path} ...")
            store_recommendation(recs[1], os.path.abspath(os.sep.join([self.output_path, f"{model.name}.tsv"])))
