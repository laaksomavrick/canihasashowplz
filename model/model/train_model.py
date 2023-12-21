from sklearn.neighbors import NearestNeighbors
from model.pipelines import get_basic_nn_pipeline
from model.functions import get_stratified_data
from joblib import dump


def start():
    train_set, test_set = get_stratified_data()
    pipeline = get_basic_nn_pipeline()
    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    knn = NearestNeighbors(metric="cosine", algorithm="auto")
    knn.fit(transposed_df)

    df_filename = "../model-inference/ratings.csv"
    model_filename = "../model-inference/model.joblib"

    dump(knn, model_filename)
    df.to_csv(df_filename, index=False)
