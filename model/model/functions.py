import re
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from os.path import dirname, join, abspath


def normalize_show_title(primary_title):
    title = re.sub(r"[^a-zA-Z0-9]", "", primary_title)
    title = title.lower()
    return title


def get_show_metadata(show_ids=[]):
    show_data_df = get_show_data()
    shows_df = show_data_df.loc[show_data_df["show_id"].isin(show_ids)]
    return shows_df["primary_title"].tolist()


def get_stratified_data(data=None):
    data = data or get_ratings_data()
    data["popularity"] = pd.cut(
        data["num_votes"],
        bins=[0, 25000, 50000, 100000, 250000, 500000, 1000000, np.inf],
        labels=[1, 2, 3, 4, 5, 6, 7],
    )

    strat_train_set, strat_test_set = stratified_shuffle(data, "popularity")

    for set_ in (strat_train_set, strat_test_set):
        set_.drop("popularity", axis=1, inplace=True)

    return strat_train_set, strat_test_set


def stratified_shuffle(data, column):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(data, data[column]):
        strat_train_set = data.loc[train_index]
        strat_test_set = data.loc[test_index]

    return strat_train_set, strat_test_set


def get_show_data():
    project_root = dirname(dirname(abspath(__file__)))
    return pd.read_csv(join(project_root, "model/data/shows.csv"))


def get_ratings_data():
    project_root = dirname(dirname(abspath(__file__)))
    return pd.read_csv(join(project_root, "model/data/ratings.csv"))
