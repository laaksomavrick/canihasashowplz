import logging
import os

import boto3

logger = logging.getLogger()

RATING_BUCKET_NAME = os.getenv("RATING_BUCKET_NAME")
RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")

MODEL_BUCKET_NAME = os.getenv("MODEL_BUCKET_NAME")

STACK_NAME = os.getenv("STACK_NAME")
MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")
MODEL_DATA_VERSION = os.getenv("MODEL_DATA_VERSION")

MODEL_TRAINING_ECR_URL = os.getenv("MODEL_TRAINING_ECR_URL")
SAGEMAKER_ROLE = os.getenv("SAGEMAKER_ROLE")


def lambda_handler(event, context):
    logger.info(f"Requesting model training job")

    sagemaker = boto3.client("sagemaker")

    training_job_name = (
        f"{STACK_NAME}-model-{MODEL_TRAINING_VERSION}-data-{MODEL_DATA_VERSION}"
    )

    environment_variables = {
        "RATING_BUCKET_NAME": RATING_BUCKET_NAME,
        "RATING_FILE_NAME": RATING_FILE_NAME,
        "MODEL_TRAINING_VERSION": MODEL_TRAINING_VERSION,
    }

    input_s3_uri = f"s3://{RATING_BUCKET_NAME}/{RATING_FILE_NAME}"
    output_bucket = f"s3://{MODEL_BUCKET_NAME}"
    instance_type = "ml.m5.4xlarge"
    instance_count = 1
    memory_volume = 8

    sagemaker.create_training_job(
        TrainingJobName=training_job_name,
        AlgorithmSpecification={
            "TrainingImage": MODEL_TRAINING_ECR_URL,
            "TrainingInputMode": "File",
        },
        RoleArn=SAGEMAKER_ROLE,
        InputDataConfig=[
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": input_s3_uri,
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
                "ContentType": "text/csv",
                "CompressionType": "None",
            }
        ],
        OutputDataConfig={"S3OutputPath": output_bucket},
        ResourceConfig={
            "InstanceType": instance_type,
            "InstanceCount": instance_count,
            "VolumeSizeInGB": memory_volume,
        },
        Environment=environment_variables,
        StoppingCondition={"MaxRuntimeInSeconds": 43200},
    )

    logger.info("Successfully requested model training job")

    return {"statusCode": 200, "body": "Successfully requested model training job"}
