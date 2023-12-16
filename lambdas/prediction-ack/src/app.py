import logging
import os
from uuid import uuid4

import boto3
import json

QUEUE_URL = os.getenv("PREDICTION_QUEUE_URL")
logger = logging.getLogger()


def lambda_handler(event, context):
    body = event["body"]
    payload = json.loads(body)
    shows = payload["shows"]

    prediction_id = str(uuid4())

    logger.info(
        f"Received request", extra={"prediction_id": prediction_id, "shows": shows}
    )

    payload = {
        "prediction_id": prediction_id,
        "show_titles": shows,
    }

    response = push_to_queue(payload)

    if response is None:
        return {
            "statusCode": 500,
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "prediction_id": prediction_id,
            }
        ),
    }


def push_to_queue(payload):
    try:
        sqs = boto3.client("sqs")

        json_payload = json.dumps(payload)

        response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json_payload)

        return response
    except Exception as e:
        logging.error(str(e))
        return None
