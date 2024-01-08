import os
import pickle

import logging

# TODO: improve logging in cw logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

STACK_NAME = os.getenv("STACK_NAME")
MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")
MODEL_DATA_VERSION = os.getenv("MODEL_DATA_VERSION")
MODEL_INFERENCE_VERSION = os.getenv("MODEL_INFERENCE_VERSION")


def load_model(model_dir):
    logger.info(f"Loading model with training_version={MODEL_TRAINING_VERSION} and data_version={MODEL_DATA_VERSION}")

    # training_job_name = f"{STACK_NAME}_model-{MODEL_TRAINING_VERSION}_data-{MODEL_DATA_VERSION}"
    # output_path = os.path.join(model_dir, training_job_name, "output")
    # logger.info(f"Path to look is {output_path}")

    graph_path = os.path.join(model_dir, f"graph-{MODEL_TRAINING_VERSION}.pkl")
    encoder_path = os.path.join(model_dir, f"label_encoder-{MODEL_TRAINING_VERSION}.pkl")
    with open(graph_path, "rb") as f:
        graph = pickle.load(f)

    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)

    return { "graph": graph, "encoder": encoder }


def get_encoded_show_ids(show_ids=[], label_encoder=None, logger=None):
    encoded_show_ids = []

    for show_id in show_ids:
        try:
            encoded_show_id = label_encoder.transform([show_id])[0]
            encoded_show_ids.append(encoded_show_id)
        except:
            logger.warn(f"Did not recognize show_id={show_id}")
            continue

    return encoded_show_ids


def predict(body, model):
    top_n = 5
    logger.info(f"Making a prediction with model_inference_version={MODEL_INFERENCE_VERSION}")
    logger.info(body)

    show_ids = body["show_ids"]

    if len(show_ids) == 0:
        return []

    graph = model["graph"]
    label_encoder = model["encoder"]

    show_ids = get_encoded_show_ids(
        show_ids=show_ids, label_encoder=label_encoder, logger=logger
    )

    similar_shows = {}

    for show_id in show_ids:
        if show_id in graph:
            neighbors = list(graph.neighbors(show_id))

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
