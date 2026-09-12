import os

os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

import boto3

from botocore.config import Config


# ============================================================
# CONFIGURATION
# ============================================================

DYNAMO_ENDPOINT = "http://localhost:4566"


# ============================================================
# TEST
# ============================================================

print("================================")
print("DYNAMODB DIRECT TEST")
print("================================")

print("Endpoint:")
print(DYNAMO_ENDPOINT)


print("\nCreating boto3 session...")

session = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

print("Boto3 session created successfully")


print("\nCreating DynamoDB configuration...")

config = Config(
    connect_timeout=5,
    read_timeout=5,
    retries={
        "max_attempts": 1
    }
)

print("Configuration created successfully")


print("\nCreating DynamoDB client...")

client = session.client(
    "dynamodb",
    endpoint_url=DYNAMO_ENDPOINT,
    config=config
)

print("DynamoDB client created successfully")


print("\nCalling list_tables...")

response = client.list_tables()

print("\n================================")
print("SUCCESS!")
print("================================")

print("Tables found:")

for table in response.get("TableNames", []):
    print(f" - {table}")


print("\nTesting scan...")

response = client.scan(
    TableName="ShiftFairTable"
)

print(
    f"Items found: {response.get('Count')}"
)

print("\n================================")
print("ALL TESTS PASSED")
print("================================")