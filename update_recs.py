import importlib
import os
from A_B_test.models import Rating
from elliot.namespace.namespace_model_builder import NameSpaceBuilder
from A_B_test_project.config import variants
from elliot.utils.write import store_recommendation
from elliot.result_handler import ResultHandler

here = os.path.abspath(os.path.dirname(__file__))


class UpdateRecs:
    def __init__(self, config_path):
        self.__builder = NameSpaceBuilder(config_path, here, os.path.abspath(os.path.dirname(config_path)))
        self.__base = self.__builder.base
        self.output_path = self.__base.base_namespace.path_output_rec_result

    def update_recs(self):
        # self.write_tsv()
        self.train_models_and_compute_recs()

    @staticmethod
    def write_tsv():
        print("Reading ratings from db ...")
        ratings = Rating.objects.all()
        tsv_ratings = []

        for r in ratings:
            tsv_ratings.append(str(r.user_id.id)+'\t'+str(r.item_id)+'\t'+str(r.rating)+'\n')

        print("Printing ratings to data/movies/ ...")
        os.makedirs("data/movies", exist_ok=True)
        with open("data/movies/dataset.tsv", "w") as f:
            f.writelines(tsv_ratings)

    def train_models_and_compute_recs(self):
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
                    self.compute_recommendations(model)
                    variants.update({f'var{count}': model})


        # recs = variants['var1'].get_single_recommendation(k=10)
        # print(recs)
        """base.base_namespace.evaluation.relevance_threshold = getattr(base.base_namespace.evaluation,
                                                                     "relevance_threshold",
                                                                     0)
        res_handler = ResultHandler(rel_threshold=base.base_namespace.evaluation.relevance_threshold)
        res_handler.save_best_results(output=base.base_namespace.path_output_rec_performance)
        cutoff_k = getattr(base.base_namespace.evaluation, "cutoffs", [base.base_namespace.top_k])
        cutoff_k = cutoff_k if isinstance(cutoff_k, list) else [cutoff_k]
        first_metric = base.base_namespace.evaluation.simple_metrics[0] if base.base_namespace.evaluation.simple_metrics else ""
        res_handler.save_best_models(output=base.base_namespace.path_output_rec_performance,
                                     default_metric=first_metric,
                                     default_k=cutoff_k)"""

    def compute_recommendations(self, model):
        recs = model.get_recommendations(self.__base.base_namespace.top_k)
        if model._save_recs:
            print(f"Writing recommendations at: {self.output_path} ...")
            store_recommendation(recs[1], os.path.abspath(os.sep.join([self.output_path, f"{model.name}.tsv"])))