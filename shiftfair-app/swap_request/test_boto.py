import json
import time
import os


os.environ["AWS_EC2_METADATA_DISABLED"] = "true"


print("=== MODULE START ===")

start = time.time()

print("Importing boto3...")

import boto3

after_import = time.time()

print(
    f"boto3 import took "
    f"{after_import - start:.2f} seconds"
)

print("Creating DynamoDB resource...")

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

after_resource = time.time()

print(
    f"DynamoDB resource creation took "
    f"{after_resource - after_import:.2f} seconds"
)


def lambda_handler(event, context):

    print("HANDLER STARTED")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "boto3 test complete"
        })
    }