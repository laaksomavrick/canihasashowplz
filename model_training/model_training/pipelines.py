from sklearn.pipeline import Pipeline

from model_training.transformers import (
    DropColumns,
    DropDuplicates,
    PivotShowIds,
    ShowUserEncoder,
    IsLikedTransformer,
)


def get_knn_pipeline(**kwargs):
    show_user_encoder = ShowUserEncoder(encoder=kwargs["label_encoder"])
    drop_duplicates = DropDuplicates(columns_to_drop_dupes=["UserId", "ShowId"])
    drop_columns = DropColumns(
        columns_to_drop=[
            "UserId",
            "ShowId",
        ]
    )
    pivot_show_ids = PivotShowIds()
    boolean_is_liked = IsLikedTransformer()

    pipeline = Pipeline(
        [
            ("drop_duplicates", drop_duplicates),
            ("show_user_encoder", show_user_encoder),
            ("drop_columns", drop_columns),
            ("boolean_is_liked", boolean_is_liked),
            ("pivot_show_ids", pivot_show_ids),
        ]
    )

    return pipeline
