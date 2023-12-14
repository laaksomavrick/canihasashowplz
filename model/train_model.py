from sklearn.neighbors import NearestNeighbors
from pipelines import get_basic_nn_pipeline
from data.functions import get_stratified_data
from joblib import dump


def start():
    train_set, test_set = get_stratified_data()
    pipeline = get_basic_nn_pipeline()
    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    knn = NearestNeighbors(metric="cosine", algorithm="auto")
    knn.fit(transposed_df)

    model_filename = "../app/model.joblib"

    dump(knn, model_filename)
