import os

import boto3
import json

QUEUE_URL = os.getenv("PREDICTION_QUEUE_URL")
SHOW_TABLE = os.getenv("SHOW_TABLE_NAME")


def push_to_queue(payload, logger):
    try:
        sqs = boto3.client("sqs")

        json_payload = json.dumps(payload)

        response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json_payload)

        return response
    except Exception as e:
        logger.error(str(e))
        return None


def get_show_ids_for_titles(show_titles):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(SHOW_TABLE)

    show_ids = []

    for title in show_titles:
        response = table.query(
            IndexName="TitleGSI",
            KeyConditionExpression="Title = :title",
            ExpressionAttributeValues={":title": title},
            ProjectionExpression="Title, ShowId",
        )

        if "Items" in response:
            for item in response["Items"]:
                show_id = item["ShowId"]
                show_ids.append(show_id)

    return show_ids
