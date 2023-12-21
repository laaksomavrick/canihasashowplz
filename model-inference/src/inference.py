import os

import joblib
import pandas as pd
import logging

logger = logging.getLogger()
df = None


def get_df():
    # TODO: read this from S3 instead
    logger.info("Retrieving ratings dataframe")
    global df
    if df is None:
        logger.info("Reading from file")
        df_file = "/opt/ml/model/ratings.csv"
        df = pd.read_csv(df_file)

    logger.info("Found ratings")
    return df

def load_model(model_dir):
    logger.info("Retrieving model")
    return joblib.load(os.path.join(model_dir, "model.joblib"))


def predict(body, model):
    logger.info("Making a prediction", extra=body)
    ratings_df = get_df()

    show_ids = body["show_ids"]

    if model is None:
        raise "Model must be set"
    if (len(ratings_df)) == 0:
        return []
    if len(show_ids) == 0:
        return []

    liked_shows_subset = ratings_df[show_ids]
    liked_shows_subset_transposed = liked_shows_subset.T

    distances, indices = model.kneighbors(liked_shows_subset_transposed, n_neighbors=3)

    similar_shows_indices = indices.flatten().tolist()
    similar_show_ids = ratings_df.columns[similar_shows_indices]
    similar_distances = distances.flatten()

    similar_shows_with_distances = dict(zip(similar_show_ids, similar_distances))
    sorted_similar_shows = sorted(
        similar_shows_with_distances.items(), key=lambda x: x[1]
    )

    sorted_show_ids = [show[0] for show in sorted_similar_shows]
    sorted_show_ids = [x for x in sorted_show_ids if x not in show_ids]

    predictions = {"predictions": sorted_show_ids}

    logger.info("Predicted", extra=predictions)

    return predictions
