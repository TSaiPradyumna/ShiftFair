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
#
# These attributes are used by the Cedar fairness policies.
# ============================================================

employees = [

    {
        "pk": "EMPLOYEE#E001",
        "sk": "PROFILE",
        "employee_id": "E001",
        "name": "Alice Johnson",
        "role": "Nurse",
        "department": "Emergency",

        # Cedar fairness attributes
        "weekly_hours": 32,
        "maximum_weekly_hours": 48,
        "skill_level": 4,
        "consecutive_working_days": 2,
        "maximum_consecutive_days": 5,
        "minimum_notice_hours": 12,
        "previous_swap_count": 1,
        "maximum_swap_count": 3,
        "experience_years": 4,
        "performance_score": 92,
        "current_night_count": 2,
        "max_night_shifts_per_week": 3,
        "minimum_rest_hours": 10
    },

    {
        "pk": "EMPLOYEE#E002",
        "sk": "PROFILE",
        "employee_id": "E002",
        "name": "Bob Smith",
        "role": "Nurse",
        "department": "Emergency",

        # Cedar fairness attributes
        "weekly_hours": 24,
        "maximum_weekly_hours": 48,
        "skill_level": 5,
        "consecutive_working_days": 1,
        "maximum_consecutive_days": 5,
        "minimum_notice_hours": 12,
        "previous_swap_count": 0,
        "maximum_swap_count": 3,
        "experience_years": 6,
        "performance_score": 95,
        "current_night_count": 1,
        "max_night_shifts_per_week": 3,
        "minimum_rest_hours": 10
    },

    {
        "pk": "EMPLOYEE#E003",
        "sk": "PROFILE",
        "employee_id": "E003",
        "name": "Carol Davis",
        "role": "Nurse",
        "department": "Emergency",

        # Cedar fairness attributes
        "weekly_hours": 40,
        "maximum_weekly_hours": 48,
        "skill_level": 3,
        "consecutive_working_days": 4,
        "maximum_consecutive_days": 5,
        "minimum_notice_hours": 12,
        "previous_swap_count": 2,
        "maximum_swap_count": 3,
        "experience_years": 3,
        "performance_score": 88,
        "current_night_count": 2,
        "max_night_shifts_per_week": 3,
        "minimum_rest_hours": 10
    },

    {
        "pk": "EMPLOYEE#E004",
        "sk": "PROFILE",
        "employee_id": "E004",
        "name": "David Wilson",
        "role": "Nurse",
        "department": "Emergency",

        # Cedar fairness attributes
        "weekly_hours": 16,
        "maximum_weekly_hours": 48,
        "skill_level": 4,
        "consecutive_working_days": 1,
        "maximum_consecutive_days": 5,
        "minimum_notice_hours": 12,
        "previous_swap_count": 0,
        "maximum_swap_count": 3,
        "experience_years": 2,
        "performance_score": 90,
        "current_night_count": 0,
        "max_night_shifts_per_week": 3,
        "minimum_rest_hours": 10
    }
]


# ============================================================
# SHIFT DATA
#
# These attributes are used by the Cedar fairness policies.
# ============================================================

shifts = [

    {
        "pk": "SHIFT#S045",
        "sk": "DETAILS",
        "shift_id": "S045",
        "employee_id": "E001",
        "date": "2026-09-15",
        "start_time": "08:00",
        "end_time": "16:00",

        # Cedar attributes
        "shift_type": "day",
        "shift_hours": 8,
        "hours_since_last_shift": 14,
        "required_skill_level": 3,
        "notice_hours": 24,
        "required_experience_years": 2,
        "minimum_performance_score": 80
    },

    {
        "pk": "SHIFT#S046",
        "sk": "DETAILS",
        "shift_id": "S046",
        "employee_id": "E002",
        "date": "2026-09-15",
        "start_time": "08:00",
        "end_time": "16:00",

        # Cedar attributes
        "shift_type": "day",
        "shift_hours": 8,
        "hours_since_last_shift": 14,
        "required_skill_level": 3,
        "notice_hours": 24,
        "required_experience_years": 2,
        "minimum_performance_score": 80
    },

    {
        "pk": "SHIFT#S050",
        "sk": "DETAILS",
        "shift_id": "S050",
        "employee_id": "E003",
        "date": "2026-09-16",
        "start_time": "08:00",
        "end_time": "16:00",

        # Cedar attributes
        "shift_type": "day",
        "shift_hours": 8,
        "hours_since_last_shift": 14,
        "required_skill_level": 3,
        "notice_hours": 24,
        "required_experience_years": 2,
        "minimum_performance_score": 80
    },

    {
        "pk": "SHIFT#S051",
        "sk": "DETAILS",
        "shift_id": "S051",
        "employee_id": "E004",
        "date": "2026-09-16",
        "start_time": "08:00",
        "end_time": "16:00",

        # Cedar attributes
        "shift_type": "day",
        "shift_hours": 8,
        "hours_since_last_shift": 14,
        "required_skill_level": 3,
        "notice_hours": 24,
        "required_experience_years": 2,
        "minimum_performance_score": 80
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
