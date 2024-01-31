import logging
from uuid import uuid4

import json
from prediction_ack.helpers import push_to_queue, get_show_ids_for_titles

logger = logging.getLogger()


def lambda_handler(event, context):
    body = event["body"]
    payload = json.loads(body)
    shows = payload.get("shows", [])

    logger.info(f"Received request", extra={"shows": shows})

    if len(shows) <= 0:
        return {"statusCode": 400}

    if len(shows) > 5:
        return {"statusCode": 400}

    show_ids = get_show_ids_for_titles(shows)

    if len(show_ids) == 0:
        logger.warning("Found no show_ids for shows", extra={"shows": shows})
        return {"statusCode": 404}

    logger.info(f"Found show_ids", extra={"show_ids": show_ids})

    prediction_id = str(uuid4())

    payload = {
        "prediction_id": prediction_id,
        "show_ids": show_ids,
    }

    response = push_to_queue(payload, logger)

    if response is None:
        logger.error(
            f"Something went wrong pushing to queue",
            extra={"prediction_id": prediction_id, "response": response},
        )
        return {
            "statusCode": 500,
        }

    logger.info(
        "Successfully pushed to queue, ending", extra={"prediction_id": prediction_id}
    )
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "prediction_id": prediction_id,
            }
        ),
        "headers": {'Access-Control-Allow-Origin': '*'}
    }
