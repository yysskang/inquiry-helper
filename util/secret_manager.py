import os
import boto3
import json


class SecretManager:
    def __init__(self: "SecretManager"):
        self.secret_name = "nursing/prod"
        self.secrets_manager_client = boto3.client(
            service_name="secretsmanager",
            region_name="ap-northeast-2",
            aws_access_key_id=os.getenv("ACCESS_KEY", ""),
            aws_secret_access_key=os.getenv("SECRET_KEY", "")
        )

    def secret_data(self, key):
        response = self.secrets_manager_client.get_secret_value(SecretId=self.secret_name)
        secret_data = json.loads(response['SecretString'])
        aws_data = secret_data.get(key, None)

        if aws_data:
            return aws_data
        else:
            return ""
