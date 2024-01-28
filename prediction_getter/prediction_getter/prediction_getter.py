import json
import logging

from prediction_getter.helpers import get_prediction, get_show_titles

logger = logging.getLogger()


def lambda_handler(event, context):
    prediction_id = event.get("queryStringParameters", {}).get("prediction_id", None)

    logger.info(
        f"Found request with prediction_id", extra={"prediction_id": prediction_id}
    )

    if prediction_id is None:
        return {"statusCode": 400}

    prediction = get_prediction(prediction_id)

    logger.info(f"Found prediction", extra={"prediction": prediction})

    if prediction is None:
        return {"statusCode": 404}

    predicted_show_ids = json.loads(prediction["Prediction"])
    predicted_show_titles = get_show_titles(predicted_show_ids, logger)

    logger.info(f"Found titles", extra={"predicted_show_titles": predicted_show_titles})

    return {
        "statusCode": 200,
        "body": json.dumps({"show_titles": predicted_show_titles}),
    }
