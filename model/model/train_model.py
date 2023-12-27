import pickle

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from model.graph import generate_graph
from model.pipelines import get_knn_graph_pipeline
from model.functions import get_stratified_data
from joblib import dump


def start():
    label_encoder = LabelEncoder()

    train_set, test_set = get_stratified_data()
    pipeline = get_knn_graph_pipeline(label_encoder=label_encoder)

    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    model = NearestNeighbors(n_neighbors=5, metric="jaccard", n_jobs=-1)
    model.fit(transposed_df)

    graph = generate_graph(model, df)

    # TODO: upload to S3 eventually
    encoder_filename = "../model-inference/label_encoder.pkl"
    graph_filename = "./graph.pkl"

    dump(label_encoder, encoder_filename)
    with open(graph_filename, "wb") as f:
        pickle.dump(graph, f)
