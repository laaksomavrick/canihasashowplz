import boto3


def main():
    s3_client = boto3.client("s3")

    file_path = "label_encoder.pkl"
    bucket_name = "canihaveatvshowplz-staging-modelbucket"
    object_name = "label_encoder.pkl"

    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(
            f"File '{file_path}' uploaded successfully to '{bucket_name}/{object_name}'"
        )
    except Exception as e:
        print(f"Failed to upload file '{file_path}' to S3: {e}")
