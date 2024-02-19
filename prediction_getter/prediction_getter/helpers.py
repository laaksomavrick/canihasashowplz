import os
import requests
import json

import boto3 as boto3

PREDICTION_TABLE_NAME = os.getenv("PREDICTION_TABLE_NAME")
SHOW_TABLE = os.getenv("SHOW_TABLE_NAME")

show_data_access_token = None


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


def get_show_info(show_name):
    info = get_show_info_from_api(show_name)

    if info is not None:
        return info

    info = get_show_info_from_api(show_name)
    # TODO: store in database
    return info


def get_show_info_from_db(show_name):
    # TODO: implement me
    return None


def get_show_info_from_api(show_name):
    url = f"https://api.themoviedb.org/3/search/tv?query={show_name}&include_adult=false&language=en-US&page=1"
    token = get_show_data_access_token()

    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)

    results = response.get("results", None)

    if results is None:
        return None

    if len(results) <= 0:
        return None

    metadata = results[0]

    image_path = metadata.get("poster_path", None)
    description = metadata.get("overview", None)
    air_date = metadata.get("first_air_date", None)
    rating = metadata.get("vote_average", None)

    return {
        "title": show_name,
        "logo_url": f"https://image.tmdb.org/t/p/w500{image_path}"
        if image_path
        else None,
        "description": description if description else None,
        "air_date": air_date if air_date else None,
        "rating": rating,
    }


def get_show_data_access_token():
    global show_data_access_token

    if show_data_access_token is not None:
        return show_data_access_token

    ssm = boto3.client("ssm")

    response = ssm.get_parameter(Name="/canihasashowplz/tmdb/api_key")

    parameter_value = response["Parameter"]["Value"]
    show_data_access_token = parameter_value
    return parameter_value
