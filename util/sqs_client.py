import json

import boto3
from django.conf import settings


class SQSClient:

    def __init__(self: "SQSClient"):
        self.sqs = boto3.client('sqs',
                                region_name=settings.AWS_S3_REGION_NAME,
                                aws_access_key_id=settings.SQS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.SQS_SECRET_ACCESS_KEY
                                )
        self.queue_url = settings.QUEUE_URL

    def send_message(self, message, group_id):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
            MessageGroupId=group_id
        )
