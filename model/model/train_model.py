import pickle

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from model.graph import generate_graph
from model.pipelines import get_knn_graph_pipeline
from model.functions import get_stratified_data
from joblib import dump

# rename "model" to "model-training"
# Get all data in Dynamo (shows, ratings)
# Configure an export (manually triggerable for the moment) to write all data in Dynamo to S3

# Update get_stratified_data to pull data from S3
# Run pipeline steps
# Save model and binary encoder to S3 with a tag that can relate data to the model and relate training code to the model
# e.g. tvshowgraph-$trainingsetid-$modelcodeidshipping
# I wonder if there is some metadata we can associate with each model for the data lineage and leave $version for id of training code

# Re-org this to accommodate SageMaker expected API; automate pushing to ECR similar to model-inference

# Write script that we can run locally to perform sagemaker_client.create_training_job
# see https://medium.com/@smertatli/aws-sagemaker-is-one-of-the-most-advanced-machine-learning-services-in-the-cloud-world-46ff67d45c0
# Eventually, we can automate this on a weekly basis via Lambda + cloudwatch event

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
