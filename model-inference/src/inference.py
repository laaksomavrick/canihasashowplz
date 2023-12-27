import io
import os
import pickle

import boto3
import logging
import joblib

# TODO: improve logging in cw logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

LABEL_ENCODER = None


def get_label_encoder_from_s3():
    bucket_name = "canihaveatvshowplz-staging-modelbucket"
    object_name = "label_encoder.pkl"
    s3 = boto3.client("s3")

    response = s3.get_object(Bucket=bucket_name, Key=object_name)

    content = response["Body"].read()

    label_encoder_file = io.BytesIO(content)

    loaded_data = joblib.load(label_encoder_file)
    return loaded_data


def get_label_encoder():
    global LABEL_ENCODER
    if LABEL_ENCODER is None:
        LABEL_ENCODER = get_label_encoder_from_s3()

    return LABEL_ENCODER


def load_model(model_dir):
    graph_path = os.path.join(model_dir, "graph.pkl")
    with open(graph_path, "rb") as f:
        loaded_graph = pickle.load(f)
        return loaded_graph


def predict(body, model):
    top_n = 5
    logger.info("Making a prediction")
    logger.info(body)

    show_ids = body["show_ids"]

    if model is None:
        raise "Model must be set"
    if len(show_ids) == 0:
        return []

    label_encoder = get_label_encoder()
    show_ids = label_encoder.transform(show_ids)

    similar_shows = {}

    for show_id in show_ids:
        if show_id in model:
            neighbors = list(model.neighbors(show_id))

            for neighbor in neighbors:
                if neighbor != show_id:
                    if neighbor in similar_shows:
                        similar_shows[neighbor] += 1
                    else:
                        similar_shows[neighbor] = 1

    sorted_shows = sorted(similar_shows.items(), key=lambda x: x[1], reverse=True)

    recommended_shows = [
        show[0] for show in sorted_shows[:top_n] if show[0] not in show_ids
    ]
    recommended_shows = label_encoder.inverse_transform(recommended_shows).tolist()

    logger.info("Made prediction")
    logger.info(recommended_shows)

    return recommended_shows
