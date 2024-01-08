import os
import pickle

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from model_training.data import stratify_ratings_data
from model_training.graph import generate_graph
from model_training.pipelines import get_knn_graph_pipeline

RATING_BUCKET_NAME = os.getenv("RATING_BUCKET_NAME")
RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")
MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")

prefix = "/opt/ml"
data_path = os.path.join(prefix, "input/data/train/")
ratings_file_path = os.path.join(data_path, RATING_FILE_NAME)
model_path = os.path.join(prefix, "model")

# TODO: Update CI for model_training ecr and sam params

# TODO: Document responsibilities in README of each re: inputs, outputs
# TODO: Create diagrams of 1) app system and 2) model training system

# TODO: Synchronize data pull + model training into a workflow via step functions
# TODO: Write script that calls step function in AWS for env (stage, prod)

# TODO: separate model training and model serving into separate stacks, document need to run training prior to running serving

# TODO: test in staging. If that works, deploy to prod and try that too.


def main():
    label_encoder = LabelEncoder()

    ratings_df = pd.read_csv(ratings_file_path)
    train_set, test_set = stratify_ratings_data(ratings_df)

    pipeline = get_knn_graph_pipeline(label_encoder=label_encoder)

    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    model = NearestNeighbors(n_neighbors=5, metric="jaccard", n_jobs=-1)
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
