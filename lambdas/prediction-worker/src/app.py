import logging
import os

import boto3 as boto3
import json

import pandas as pd

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")
logger = logging.getLogger()

def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["body"])
        prediction_id = payload["prediction_id"]
        show_titles = payload["show_titles"]

        logger.info(
            f"Received prediction request",
            extra={"prediction_id": prediction_id, "show_titles": show_titles},
        )

        # TODO: write rating to dynamodb (show_id, user_id (prediction_id), IsLiked: 1)

        # TODO: get show ids from payload
        show_ids = [
            "365563,9c7a19bc-6f54-4d21-b6b6-0606e29fbba3",
            "447316,8c0ebcc3-fbf7-4a67-8c3e-85f13de11f8e",
        ]

        # TODO: call SageMaker endpoint

        # logger.info(
        #     f"Made prediction",
        #     extra={"prediction_id": prediction_id, "prediction": prediction},
        # )
        #
        # write_to_dynamodb(PREDICTION_TABLE_NAME, prediction_id, prediction)
        #
        # logger.info(
        #     "Wrote prediction to dynamo", extra={"prediction_id": prediction_id}
        # )

    return {
        "statusCode": 200,
    }


def write_to_dynamodb(table_name, prediction_id, prediction):
    dynamodb = boto3.client("dynamodb")

    item = {
        "PredictionId": {"S": prediction_id},
        "Prediction": {"S": prediction},
    }

    try:
        response = dynamodb.put_item(TableName=table_name, Item=item)

        return response

    except Exception as e:
        logging.error(str(e))
        return None


def predict_nearest_neighbor(show_ids, model=None, df=pd.DataFrame(data={})):
    if model is None:
        raise "Model must be set"
    if (len(df)) == 0:
        return []
    if len(show_ids) == 0:
        return []

    liked_shows_subset = df[show_ids]
    liked_shows_subset_transposed = liked_shows_subset.T

    distances, indices = model.kneighbors(liked_shows_subset_transposed, n_neighbors=3)

    # Rank based on distance
    similar_shows_indices = indices.flatten().tolist()
    similar_show_ids = df.columns[similar_shows_indices]
    similar_distances = distances.flatten()

    similar_shows_with_distances = dict(zip(similar_show_ids, similar_distances))
    sorted_similar_shows = sorted(
        similar_shows_with_distances.items(), key=lambda x: x[1]
    )

    sorted_show_ids = [show[0] for show in sorted_similar_shows]

    # Filter shows included in provided show_ids
    sorted_show_ids = [x for x in sorted_show_ids if x not in show_ids]

    return sorted_show_ids
