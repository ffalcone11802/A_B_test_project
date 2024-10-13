from enum import Enum

DATASETS_PATH = 'datasets/'


class DataSet(Enum):
    ITEMS = DATASETS_PATH + 'items.csv'
    USERS = DATASETS_PATH + 'users.csv'
    RECOMMENDATIONS = DATASETS_PATH + 'recommendations.csv'
