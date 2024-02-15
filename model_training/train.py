import os
import pickle

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from model_training.graph import generate_graph
from model_training.pipelines import get_knn_pipeline

RATING_BUCKET_NAME = os.getenv("RATING_BUCKET_NAME")
RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")
MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")

prefix = "/opt/ml"
data_path = os.path.join(prefix, "input/data/train/")
ratings_file_path = os.path.join(data_path, RATING_FILE_NAME)
model_path = os.path.join(prefix, "model")


def main():
    label_encoder = LabelEncoder()

    train_set = pd.read_csv(ratings_file_path)

    pipeline = get_knn_pipeline(label_encoder=label_encoder)

    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    model = NearestNeighbors(n_neighbors=5, metric="cosine", algorithm="brute", n_jobs=-1)
    model.fit(transposed_df)

    graph = generate_graph(model, df)

    graph_filename = f"graph-{MODEL_TRAINING_VERSION}.pkl"
    encoder_filename = f"label_encoder-{MODEL_TRAINING_VERSION}.pkl"

    with open(os.path.join(model_path, graph_filename), "wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(model_path, encoder_filename), "wb") as handle:
        pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
