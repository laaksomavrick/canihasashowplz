import json
import os
import uuid

import boto3 as boto3

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")
SHOW_TABLE = os.getenv("SHOW_TABLE_NAME")


def get_prediction(prediction_id):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(PREDICTION_TABLE_NAME)

    response = table.get_item(Key={"PredictionId": prediction_id})

    if "Item" not in response:
        return None

    item = response["Item"]
    return item


def get_show_titles(show_ids, logger):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(SHOW_TABLE)

    show_titles = []

    for show_id in show_ids:
        response = table.get_item(Key={"ShowId": show_id})

        if "Item" not in response:
            logger.error(
                f"Received show id where no show exists", extra={"show_id": show_id}
            )
            continue

        item = response["Item"]
        title = item["HumanTitle"]
        show_titles.append(title)

    return show_titles
