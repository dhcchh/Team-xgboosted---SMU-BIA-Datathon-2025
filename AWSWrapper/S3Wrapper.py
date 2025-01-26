import boto3
import os

from dotenv import load_dotenv

class S3Wrapper:
    def __init__(
            self,
            region: str = "ap-southeast-1"
    ):
        load_dotenv()
        self.region = region
        self.client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )

    def send_data(
            self,
            file: str,
            bucket: str,
            s3_key: str = None
    ):
        self.client.upload_file(
            filename=file,
            bucket_name=bucket,
            key=s3_key if s3_key else file
        )

    def get_data_s3(
    ):
        print("To be implemented!")
        raise NotImplementedError