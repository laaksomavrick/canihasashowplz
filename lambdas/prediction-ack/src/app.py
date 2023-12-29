import logging
from uuid import uuid4

import json

from src.helpers import push_to_queue

logger = logging.getLogger()


def lambda_handler(event, context):
    body = event["body"]
    payload = json.loads(body)
    shows = payload.get("shows", [])

    if len(shows) == 0:
        return {"statusCode": 400}

    prediction_id = str(uuid4())

    logger.info(
        f"Received request", extra={"prediction_id": prediction_id, "shows": shows}
    )

    payload = {
        "prediction_id": prediction_id,
        "show_titles": shows,
    }

    response = push_to_queue(payload, logger)

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
