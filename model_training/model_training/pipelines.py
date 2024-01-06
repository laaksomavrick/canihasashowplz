from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from model_training.transformers import (
    AddIsLikedAttribute,
    DropColumns,
    DropDuplicates,
    PivotShowIds,
    AddGraphPartitionIdAttribute,
    ShowUserEncoder,
    JaccardDistanceTransformer,
)


def get_basic_nn_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_columns = DropColumns(
        columns_to_drop=[
            "rating",
            "primary_title",
            "start_year",
            "end_year",
            "genres",
            "average_rating",
            "num_votes",
        ]
    )
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])
    pivot_show_ids = PivotShowIds()

    pipeline = Pipeline(
        [
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
            ("drop_duplicates", drop_duplicates),
            ("pivot_show_ids", pivot_show_ids),
        ]
    )

    return pipeline


def get_knn_graph_pipeline(**kwargs):
    show_user_encoder = ShowUserEncoder(encoder=kwargs["label_encoder"])
    add_is_liked_attr = AddIsLikedAttribute()
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])
    drop_columns = DropColumns(
        columns_to_drop=[
            "rating",
            "primary_title",
            "start_year",
            "end_year",
            "genres",
            "average_rating",
            "num_votes",
            "user_id",
            "show_id",
        ]
    )
    pivot_show_ids = PivotShowIds()

    pipeline = Pipeline(
        [
            ("drop_duplicates", drop_duplicates),
            ("add_is_liked_attr", add_is_liked_attr),
            ("show_user_encoder", show_user_encoder),
            ("drop_columns", drop_columns),
            ("pivot_show_ids", pivot_show_ids),
        ]
    )

    return pipeline


def get_jaccard_distance_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])
    drop_columns = DropColumns(
        columns_to_drop=[
            "rating",
            "primary_title",
            "start_year",
            "end_year",
            "genres",
            "average_rating",
            "num_votes",
        ]
    )
    jaccard_distance = JaccardDistanceTransformer()

    pipeline = Pipeline(
        [
            ("drop_duplicates", drop_duplicates),
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
            ("jaccard_distance", jaccard_distance),
        ]
    )

    return pipeline


def get_high_quality_nn_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_columns = DropColumns(
        columns_to_drop=[
            "rating",
            "primary_title",
            "start_year",
            "end_year",
            "genres",
            "average_rating",
            "num_votes",
        ]
    )
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])

    def filter_by_rating(df):
        return df[df["average_rating"] >= 7.0]

    filter_only_high_quality_shows = FunctionTransformer(filter_by_rating)

    pipeline = Pipeline(
        [
            ("filter_only_high_quality_shows", filter_only_high_quality_shows),
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
            ("drop_duplicates", drop_duplicates),
        ]
    )

    return pipeline


def get_cluster_labeled_nn_pipeline():
    add_is_liked_attr = AddIsLikedAttribute()
    drop_columns = DropColumns(
        columns_to_drop=["rating", "primary_title", "end_year", "genres", "num_votes"]
    )
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["user_id", "show_id"])
    add_graph_partition_id_attr = AddGraphPartitionIdAttribute()

    pipeline = Pipeline(
        [
            ("add_is_liked_attr", add_is_liked_attr),
            ("drop_columns", drop_columns),
            ("drop_duplicates", drop_duplicates),
            ("add_graph_partition_id_attr", add_graph_partition_id_attr),
        ]
    )

    return pipeline
