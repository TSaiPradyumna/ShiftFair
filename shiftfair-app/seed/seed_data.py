import os
import boto3
from botocore.exceptions import ClientError


# ============================================================
# CONFIGURATION
# ============================================================

DYNAMO_ENDPOINT = os.environ.get(
    "DYNAMO_ENDPOINT",
    "http://localhost:4566"
)

TABLE_NAME = os.environ.get(
    "TABLE_NAME",
    "ShiftFairTable"
)


# ============================================================
# DYNAMODB CONNECTION
# ============================================================

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMO_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table(TABLE_NAME)


# ============================================================
# EMPLOYEE DATA
# ============================================================

employees = [

    {
        "pk": "EMPLOYEE#E001",
        "sk": "PROFILE",
        "employee_id": "E001",
        "name": "Alice Johnson",
        "role": "Nurse",
        "department": "Emergency"
    },

    {
        "pk": "EMPLOYEE#E002",
        "sk": "PROFILE",
        "employee_id": "E002",
        "name": "Bob Smith",
        "role": "Nurse",
        "department": "Emergency"
    },

    {
        "pk": "EMPLOYEE#E003",
        "sk": "PROFILE",
        "employee_id": "E003",
        "name": "Carol Davis",
        "role": "Nurse",
        "department": "Emergency"
    },

    {
        "pk": "EMPLOYEE#E004",
        "sk": "PROFILE",
        "employee_id": "E004",
        "name": "David Wilson",
        "role": "Nurse",
        "department": "Emergency"
    }
]


# ============================================================
# SHIFT DATA
# ============================================================

shifts = [

    {
        "pk": "SHIFT#S045",
        "sk": "DETAILS",
        "shift_id": "S045",
        "employee_id": "E001",
        "date": "2026-09-15",
        "start_time": "08:00",
        "end_time": "16:00"
    },

    {
        "pk": "SHIFT#S046",
        "sk": "DETAILS",
        "shift_id": "S046",
        "employee_id": "E002",
        "date": "2026-09-15",
        "start_time": "08:00",
        "end_time": "16:00"
    },

    {
        "pk": "SHIFT#S050",
        "sk": "DETAILS",
        "shift_id": "S050",
        "employee_id": "E003",
        "date": "2026-09-16",
        "start_time": "08:00",
        "end_time": "16:00"
    },

    {
        "pk": "SHIFT#S051",
        "sk": "DETAILS",
        "shift_id": "S051",
        "employee_id": "E004",
        "date": "2026-09-16",
        "start_time": "08:00",
        "end_time": "16:00"
    }
]


# ============================================================
# INSERT DATA
# ============================================================

def seed_data():

    print("================================")
    print("Seeding ShiftFair DynamoDB Data")
    print("================================")

    try:

        print("\nInserting employees...")

        for employee in employees:

            table.put_item(
                Item=employee
            )

            print(
                f"Inserted employee: "
                f"{employee['employee_id']} "
                f"({employee['name']})"
            )

        print("\nInserting shifts...")

        for shift in shifts:

            table.put_item(
                Item=shift
            )

            print(
                f"Inserted shift: "
                f"{shift['shift_id']} "
                f"for "
                f"{shift['employee_id']}"
            )

        print("\n================================")
        print("Database seeded successfully!")
        print("================================")

    except ClientError as e:

        print("\nDynamoDB error:")

        print(
            e.response["Error"]["Message"]
        )


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":

    seed_data()