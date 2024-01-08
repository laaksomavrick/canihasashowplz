import s3fs
import pandas as pd
from sklearn.model_selection import train_test_split


def get_ratings_data(bucket_name, file_key):
    s3 = s3fs.S3FileSystem()
    ratings_file_path = f"s3://{bucket_name}/{file_key}"
    with s3.open(ratings_file_path, "rb") as f:
        df = pd.read_csv(f)
        return df


def stratify_ratings_data(ratings_df):
    unique_show_ids = ratings_df["ShowId"].nunique()
    train_size = int(unique_show_ids * 0.8)

    train_data = ratings_df.groupby("IsLiked", group_keys=False).apply(
        lambda x: x.sample(min(len(x), train_size))
    )
    test_data = ratings_df.drop(train_data.index)

    train_data = train_data[ratings_df.columns]
    test_data = test_data[ratings_df.columns]

    return [train_data, test_data]
