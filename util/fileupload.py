import os
import boto3
from django.conf import settings
from django.utils.timezone import now


class S3Client:

    def __init__(self: "S3Client"):
        self.s3_client = boto3.client('s3',
                                      region_name=settings.AWS_S3_REGION_NAME,
                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                      )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def file_upload(self, file_obj, api_key):
        from datetime import datetime
        formatted_date = datetime.now().strftime("%Y%m%d")
        original_file_name, file_extension = os.path.splitext(file_obj.name)
        safe_file_name = f"{original_file_name}_{now().strftime('%Y%m%d%H%M%S')}{file_extension}"

        file_key = f"{api_key}/{formatted_date}/{safe_file_name}"
        self.s3_client.upload_fileobj(
            file_obj,
            self.bucket_name,
            file_key,
            ExtraArgs={'ContentType': file_obj.content_type, 'ACL': 'private'}
        )

        return f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_key}"

