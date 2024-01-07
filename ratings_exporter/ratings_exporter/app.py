import csv
import logging
import os
import boto3
import s3fs

logger = logging.getLogger()

DESTINATION_BUCKET_NAME = os.getenv("DESTINATION_BUCKET_NAME")
RATING_TABLE_NAME = os.getenv("RATING_TABLE_NAME")
RATING_FILE_NAME = os.getenv("RATING_FILE_NAME")

def lambda_handler(event, context):
    logger.info(f"Exporting ratings to bucket", extra={"bucket": DESTINATION_BUCKET_NAME, "table": RATING_TABLE_NAME, "key": RATING_FILE_NAME})

    dynamodb = boto3.resource('dynamodb')
    s3 = s3fs.S3FileSystem()

    table = dynamodb.Table(RATING_TABLE_NAME)
    headers = get_headers()

    with s3.open(f'{DESTINATION_BUCKET_NAME}/{RATING_FILE_NAME}', 'w') as s3_file:
        csv_writer = csv.writer(s3_file)
        csv_writer.writerow(headers)

        response = table.scan()
        while 'Items' in response:
            for item in response['Items']:
                row = [item['UserId'], item['ShowId'], item['IsLiked']]
                csv_writer.writerow(row)

            if 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            else:
                break

    logger.info("Data exported to S3 successfully")

    return {
        'statusCode': 200,
        'body': 'Data exported to S3 successfully'
    }

def get_headers():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(RATING_TABLE_NAME)
    response = table.scan(Limit=1)
    items = response['Items']

    if len(items) == 0:
        raise "Can not determine headers for the file"

    headers = list(items[0].keys())
    return headers