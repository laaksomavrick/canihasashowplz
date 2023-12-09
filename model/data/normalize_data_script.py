from uuid import uuid4
from os.path import abspath, dirname, join
from pandas import read_csv


def start():
    project_root = dirname(dirname(abspath(__file__)))
    shows_df = read_csv(join(project_root, "data/imdb_shows.csv"))
    ratings_df = read_csv(join(project_root, "data/imdb_ratings.csv"))

    show_id_mapping = {}
    user_id_mapping = {}

    for df in [shows_df, ratings_df]:
        for index, row in df.iterrows():
            old_show_id = row["show_id"]
            if old_show_id not in show_id_mapping:
                show_id_mapping[old_show_id] = str(uuid4())

    for index, row in ratings_df.iterrows():
        old_user_id = row["user_id"]
        if old_user_id not in user_id_mapping:
            user_id_mapping[old_user_id] = str(uuid4())

    for df in [shows_df, ratings_df]:
        df["show_id"] = df["show_id"].map(show_id_mapping)

    ratings_df["user_id"] = ratings_df["user_id"].map(user_id_mapping)

    shows_df.to_csv(join(project_root, "data/shows.csv"), index=False)
    ratings_df.to_csv(join(project_root, "data/ratings.csv"), index=False)
