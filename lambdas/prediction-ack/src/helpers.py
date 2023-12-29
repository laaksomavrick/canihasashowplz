import os

import boto3
import json

QUEUE_URL = os.getenv("PREDICTION_QUEUE_URL")


def push_to_queue(payload, logger):
    try:
        sqs = boto3.client("sqs")

        json_payload = json.dumps(payload)

        response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json_payload)

        return response
    except Exception as e:
        logger.error(str(e))
        return None
