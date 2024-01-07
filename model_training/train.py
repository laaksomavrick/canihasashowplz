import os
import pickle

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from model_training.data import get_ratings_data, stratify_ratings_data
from model_training.graph import generate_graph
from model_training.pipelines import get_knn_graph_pipeline

RATING_BUCKET_NAME = os.getenv("RATING_BUCKET_NAME")
RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")
MODEL_BUCKET_NAME = os.getenv("MODEL_BUCKET_NAME")
MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")

# In a docker container made for sagemaker training:
# Update get_stratified_data to pull data from S3 via an ENV variable we'll later inject in cfn
# Run pipeline steps
# Save model and binary encoder to S3 with a tag that can relate data to the model and relate training code to the model
# e.g. tvshowgraph-$trainingsetid-$modelcodeidshipping
# Re-org this to accommodate SageMaker expected API; automate pushing to ECR similar to model-inference

# TODO: Write lambda that we can run to perform sagemaker_client.create_training_job via this container
# see https://medium.com/@smertatli/aws-sagemaker-is-one-of-the-most-advanced-machine-learning-services-in-the-cloud-world-46ff67d45c0

# TODO: Document responsibilities in README of each re: inputs, outputs
# TODO: Create diagrams of 1) app system and 2) model training system

# TODO: Update CI

# TODO: Synchronize data pull + model training into a workflow via step functions

# TODO: test in staging. If that works, deploy to prod and try that too.

def main():
    label_encoder = LabelEncoder()

    ratings_df = get_ratings_data(RATING_BUCKET_NAME, RATING_FILE_NAME)
    train_set, test_set = stratify_ratings_data(ratings_df)

    pipeline = get_knn_graph_pipeline(label_encoder=label_encoder)

    df = pipeline.fit_transform(train_set)
    transposed_df = df.T

    model = NearestNeighbors(n_neighbors=5, metric="jaccard", n_jobs=-1)
    model.fit(transposed_df)

    graph = generate_graph(model, df)

    graph_filename = f"./graph-{MODEL_TRAINING_VERSION}.pkl"
    encoder_filename = f'./label_encoder-{MODEL_TRAINING_VERSION}.pkl'

    with open(graph_filename, "wb") as f:
        pickle.dump(graph, f)

    with open(encoder_filename, "wb") as f:
        pickle.dump(label_encoder, f)


if __name__ == "__main__":
    main()
