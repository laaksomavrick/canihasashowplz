from os.path import abspath, dirname, join
from pandas import read_csv
from boto3 import resource


def start():
    print(
        "Importing prod data into prod tables - make sure your shell has AWS_PROFILE set!"
    )
    dynamodb = resource("dynamodb")
    shows_table = dynamodb.Table("canihaveatvshowplz-prod-ShowsV1")
    ratings_table = dynamodb.Table("canihaveatvshowplz-prod-RatingsV1")

    [shows, ratings] = get_data()

    with shows_table.batch_writer() as batch:
        for item in shows:
            batch.put_item(Item=item)

    with ratings_table.batch_writer() as batch:
        for item in ratings:
            batch.put_item(Item=item)

    print("All done!")


def get_data():
    project_root = dirname(dirname(abspath(__file__)))
    shows_df = read_csv(join(project_root, "data/shows.csv"))
    ratings_df = read_csv(join(project_root, "data/ratings.csv"))

    top_shows = shows_df.sort_values("num_votes", ascending=False).to_dict(
        orient="records"
    )
    top_show_ids = [show["show_id"] for show in top_shows]

    ratings_for_top_shows = ratings_df[
        ratings_df["show_id"].isin(top_show_ids)
    ].to_dict(orient="records")

    top_shows = list(
        map(
            lambda show: {"ShowId": show["show_id"], "Title": show["normalized_title"]},
            top_shows,
        )
    )
    ratings_for_top_shows = list(
        map(
            lambda rating: {
                "ShowId": rating["show_id"],
                "UserId": rating["user_id"],
                "IsLiked": rating["is_liked"],
            },
            ratings_for_top_shows,
        )
    )

    return [top_shows, ratings_for_top_shows]
