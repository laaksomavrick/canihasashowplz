import logging
import os
import time

import boto3

logger = logging.getLogger()

# RATING_BUCKET_NAME = os.getenv("RATING_BUCKET_NAME")
# RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")
#
# MODEL_BUCKET_NAME = os.getenv("MODEL_BUCKET_NAME")
#
# STACK_NAME = os.getenv("STACK_NAME")
# MODEL_TRAINING_VERSION = os.getenv("MODEL_TRAINING_VERSION")
# MODEL_DATA_VERSION = os.getenv("MODEL_DATA_VERSION")
#
# MODEL_TRAINING_ECR_URL = os.getenv("MODEL_TRAINING_ECR_URL")
# SAGEMAKER_ROLE = os.getenv("SAGEMAKER_ROLE")

RATING_BUCKET_NAME = 'canihaveatvshowplz-staging-ratingsexport'
RATING_FILE_NAME = 'ratings-1.0.0.csv'

MODEL_BUCKET_NAME = 'canihaveatvshowplz-staging-modelbucket'

STACK_NAME = 'canihaveatvshowplz'
MODEL_TRAINING_VERSION = '1.0.0'

MODEL_TRAINING_ECR_URL = '844544735981.dkr.ecr.ca-central-1.amazonaws.com/canihaveatvshowplz-staging/modeltrainingrepo:1.0.0'
SAGEMAKER_ROLE = 'arn:aws:iam::844544735981:role/canihaveatvshowplz-staging-SageMakerExecutionRole-nVy1TkCYuyEP'

def lambda_handler(event, context):
    # logger.info(f"Requesting model training job", extra={"bucket": DESTINATION_BUCKET_NAME, "table": RATING_TABLE_NAME, "key": RATING_FILE_NAME})

    sagemaker = boto3.client("sagemaker")

    # TODO: want a more deterministic way of setting this
    # e.g., from version file indicating a "run-id"?
    training_job_name = f"{STACK_NAME}-{time.strftime('%Y-%m-%d-%H-%M-%S')}"

    environment_variables = {
        'RATING_BUCKET_NAME': RATING_BUCKET_NAME,
        'RATING_FILE_NAME': RATING_FILE_NAME,
        'MODEL_TRAINING_VERSION': MODEL_TRAINING_VERSION
    }

    input_s3_uri = f"s3://{RATING_BUCKET_NAME}/{RATING_FILE_NAME}"
    output_bucket = f"s3://{MODEL_BUCKET_NAME}"
    instance_type = 'ml.m5.4xlarge'
    instance_count = 1
    memory_volume = 8

    sagemaker.create_training_job(
        TrainingJobName=training_job_name,
        AlgorithmSpecification={
            'TrainingImage': MODEL_TRAINING_ECR_URL,
            'TrainingInputMode': 'File'
        },
        RoleArn=SAGEMAKER_ROLE,
        InputDataConfig=[{
            'ChannelName': 'train',
            'DataSource': {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": input_s3_uri,
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            'ContentType': 'text/csv',
            'CompressionType': 'None'
        }],
        OutputDataConfig={"S3OutputPath": output_bucket},
        ResourceConfig={
            "InstanceType": instance_type,
            "InstanceCount": instance_count,
            "VolumeSizeInGB": memory_volume
        },
        Environment=environment_variables,
        StoppingCondition={'MaxRuntimeInSeconds': 43200}
    )

    logger.info("Successfully requested model training job")

    return {
        'statusCode': 200,
        'body': 'Data exported to S3 successfully'
    }