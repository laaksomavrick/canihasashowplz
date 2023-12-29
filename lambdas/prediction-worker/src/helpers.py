import json
import os
import uuid

import boto3 as boto3

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")
RATING_TABLE_NAME = os.getenv("RATING_TABLE_NAME")
SAGEMAKER_ENDPOINT_NAME = os.getenv("PREDICTION_ENDPOINT_NAME")


def save_prediction(prediction_id, prediction):
    dynamodb = boto3.client("dynamodb")

    item = {
        "PredictionId": {"S": prediction_id},
        "Prediction": {"S": json.dumps(prediction)},
    }

    response = dynamodb.put_item(TableName=PREDICTION_TABLE_NAME, Item=item)

    return response


def get_prediction(show_ids=[]):
    runtime = boto3.client("sagemaker-runtime")

    payload = {"show_ids": show_ids}
    payload_json = json.dumps(payload)

    response = runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT_NAME,
        ContentType="application/json",
        Body=payload_json,
    )

    result = json.loads(response["Body"].read().decode())

    return result


def write_is_liked(show_ids):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(RATING_TABLE_NAME)

    # TODO: support user_id as param from FE
    user_id = str(uuid.uuid4())
    is_liked = True

    for show_id in show_ids:
        item = {"ShowId": str(show_id), "UserId": user_id, "IsLiked": is_liked}

        table.put_item(Item=item)
