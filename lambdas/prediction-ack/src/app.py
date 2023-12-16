import logging
import os
from uuid import uuid4

import boto3
import json

import boto3 as boto3


def lambda_handler(event, context):
    body = event["body"]
    print(body)

    request_id = uuid4()

    payload = {
        "request_id": request_id,
        "show_titles": ["The Wire", "The Sopranos"],  # TODO: read from request body
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
                "prediction_id": request_id,
            }
        ),
    }


def push_to_queue(payload):
    try:
        queue_url = os.getenv("PREDICTION_QUEUE_URL")
        sqs = boto3.client("sqs")

        json_payload = json.dumps(payload)

        response = sqs.send_message(QueueUrl=queue_url, MessageBody=json_payload)

        return response
    except Exception as e:
        logging.error(str(e))
        return None
