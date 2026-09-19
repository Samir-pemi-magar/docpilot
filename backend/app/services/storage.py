import boto3
from botocore.exceptions import ClientError

from app.core.config import settings


class StorageService:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.minio_endpoint,
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
        )

        self.bucket = settings.minio_bucket

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code in ("404", "NoSuchBucket"):
                self.client.create_bucket(Bucket=self.bucket)
            else:
                raise

    def upload_file(
        self,
        file_object,
        object_key: str,
        content_type: str,
    ) -> None:
        self.client.upload_fileobj(
            file_object,
            self.bucket,
            object_key,
            ExtraArgs={
                "ContentType": content_type,
            },
        )

    def download_file(
        self,
        object_key: str,
        file_object,
    ) -> None:
        self.client.download_fileobj(
            self.bucket,
            object_key,
            file_object,
        )

    def delete_file(self, object_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket,
            Key=object_key,
        )


storage_service = StorageService()