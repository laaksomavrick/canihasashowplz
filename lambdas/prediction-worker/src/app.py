import logging
import os

import boto3 as boto3
import json

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")
SAGEMAKER_ENDPOINT_NAME = os.getenv("PREDICTION_ENDPOINT_NAME")
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
            "b442937f-19dc-4429-96f5-6d4b6e733f2c",
            "387c6565-98ab-4342-ae8e-fb7faef78af0",
        ]

        prediction = get_prediction(show_ids)

        logger.info(
            f"Made prediction",
            extra={"prediction_id": prediction_id, "prediction": prediction},
        )

        save_prediction(PREDICTION_TABLE_NAME, prediction_id, prediction)

        logger.info(
            "Wrote prediction to dynamo", extra={"prediction_id": prediction_id}
        )

    return {
        "statusCode": 200,
    }


def save_prediction(table_name, prediction_id, prediction):
    dynamodb = boto3.client("dynamodb")

    item = {
        "PredictionId": {"S": prediction_id},
        "Prediction": {"S": json.dumps(prediction)},
    }

    try:
        response = dynamodb.put_item(TableName=table_name, Item=item)

        return response

    except Exception as e:
        logging.error(str(e))
        return None


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
