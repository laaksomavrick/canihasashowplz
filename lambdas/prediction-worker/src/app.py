import logging
import os

import boto3 as boto3
import joblib
import json

model_file = "/opt/ml/model"
model = joblib.load(model_file)

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")


def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["body"])
        prediction_id = payload["prediction_id"]
        show_titles = payload["show_titles"]

        # TODO: log json for cloudwatch logs via python-json-logger or similar
        logging.info(
            f"Received prediction request: prediction_id={prediction_id} show_titles={show_titles}"
        )

        # TODO: get show ids from payload
        prediction = model.predict(
            [
                "365563,9c7a19bc-6f54-4d21-b6b6-0606e29fbba3",
                "447316,8c0ebcc3-fbf7-4a67-8c3e-85f13de11f8e",
            ]
        )

        write_to_dynamodb(PREDICTION_TABLE_NAME, prediction_id, prediction)

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
