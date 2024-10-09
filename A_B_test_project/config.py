from enum import Enum

DATABASE = {}

DATASETS_PATH = 'datasets/'


class Variant(Enum):
    A = 'endpointA'
    B = 'endpointB'


class DataSet(Enum):
    ITEMS = DATASETS_PATH + 'items.csv'
    USERS = DATASETS_PATH + 'users.csv'
    RECOMMENDATIONS = DATASETS_PATH + 'recommendations.csv'
