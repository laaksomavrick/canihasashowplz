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


def get_shows(show_ids, logger):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(SHOW_TABLE)

    shows = []

    for show_id in show_ids:
        response = table.get_item(Key={"ShowId": show_id})

        if "Item" not in response:
            logger.error(
                f"Received show id where no show exists", extra={"show_id": show_id}
            )
            continue

        item = response["Item"]

        normalized_title = item.get("HumanTitle", None)

        logo_url = item.get("LogoUrl", None)
        description = item.get("Description", None)
        air_date = item.get("AirDate", None)
        rating = item.get("Rating", None)

        logger.info("Found show for id", extra={"show": item})

        if (
            logo_url is None
            or description is None
            or air_date is None
            or rating is None
        ):
            logger.info(
                "Attempting to retrieve more metadata for show",
                extra={"show_id": show_id},
            )
            show_metadata = get_show_info_from_api(normalized_title, logger)
            update_show(item, show_metadata)
            response = table.get_item(Key={"ShowId": show_id})
            item = response["Item"]

        show_data = {
            "id": item["ShowId"],
            "title": item["HumanTitle"],
            "normalized_title": item["Title"],
            "logo_url": item["LogoUrl"],
            "description": item["Description"],
            "air_date": item["AirDate"],
            "rating": item["Rating"],
        }
        shows.append(show_data)

    return shows


def update_show(show, show_metadata):
    dynamodb = boto3.client("dynamodb")

    item = {
        "ShowId": {"S": show["ShowId"]},
        "HumanTitle": {"S": show["HumanTitle"]},
        "Title": {"S": show["Title"]},
        "LogoUrl": {"S": show_metadata["logo_url"]},
        "Description": {"S": show_metadata["description"]},
        "AirDate": {"S": show_metadata["air_date"]},
        "Rating": {"S": str(show_metadata["rating"])},
    }

    response = dynamodb.put_item(TableName=SHOW_TABLE, Item=item)

    return response


def get_show_info_from_api(show_name, logger):
    url = f"https://api.themoviedb.org/3/search/tv"

    query_params = {
        "query": show_name,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
    }
    token = get_show_data_access_token()

    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, params=query_params)
    response = json.loads(response.text)

    results = response.get("results", None)

    logger.info(
        "Found response for show metadata retrieval", extra={"results": results}
    )

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
