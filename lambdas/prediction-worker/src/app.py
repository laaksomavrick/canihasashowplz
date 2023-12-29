import logging
import json

from src.helpers import write_is_liked, get_prediction, save_prediction

logger = logging.getLogger()


def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["body"])
        prediction_id = payload["prediction_id"]
        show_ids = payload["show_ids"]

        logger.info(
            f"Received prediction request",
            extra={"prediction_id": prediction_id, "show_ids": show_ids},
        )

        write_is_liked(show_ids)

        logger.info(
            f"Wrote is liked",
            extra={"prediction_id": prediction_id, "show_ids": show_ids},
        )

        prediction = get_prediction(show_ids)

        logger.info(
            f"Made prediction",
            extra={"prediction_id": prediction_id, "prediction": prediction},
        )

        save_prediction(prediction_id, prediction)

        logger.info(
            "Wrote prediction to dynamo", extra={"prediction_id": prediction_id}
        )

    return {
        "statusCode": 200,
    }
