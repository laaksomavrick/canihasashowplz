from uuid import uuid4
from os.path import abspath, dirname, join
from pandas import read_csv


def start():
    project_root = dirname(dirname(abspath(__file__)))
    shows_df = read_csv(join(project_root, "data/imdb_shows.csv"))
    ratings_df = read_csv(join(project_root, "data/imdb_ratings.csv"))

    id_mapping = {}

    for df in [shows_df, ratings_df]:
        for index, row in df.iterrows():
            old_id = row["show_id"]
            if old_id not in id_mapping:
                id_mapping[old_id] = str(uuid4())

    for df in [shows_df, ratings_df]:
        df["show_id"] = df["show_id"].map(id_mapping)

    shows_df.to_csv(join(project_root, "data/shows.csv"), index=False)
    ratings_df.to_csv(join(project_root, "data/ratings.csv"), index=False)
