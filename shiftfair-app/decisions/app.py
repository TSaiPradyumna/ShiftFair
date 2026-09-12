import json
import os
import time

from decimal import Decimal

os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

import boto3

from botocore.config import Config

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    ConnectTimeoutError,
    ReadTimeoutError
)


# ============================================================
# CONFIGURATION
# ============================================================

DYNAMO_ENDPOINT = os.environ.get(
    "DYNAMO_ENDPOINT",
    "http://host.docker.internal:4566"
)

TABLE_NAME = os.environ.get(
    "TABLE_NAME",
    "ShiftFairTable"
)


# ============================================================
# DYNAMODB CONNECTION
# ============================================================

def get_dynamodb_resource():

    print(
        "Inside get_dynamodb_resource()"
    )

    print(
        f"Using endpoint: {DYNAMO_ENDPOINT}"
    )

    print(
        "Creating explicit boto3 session..."
    )

    session = boto3.Session(
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    print(
        "Boto3 session created"
    )

    dynamodb_config = Config(

        connect_timeout=5,

        read_timeout=5,

        retries={
            "max_attempts": 1
        }
    )

    print(
        "Creating DynamoDB resource..."
    )

    dynamodb = session.resource(

        "dynamodb",

        endpoint_url=DYNAMO_ENDPOINT,

        config=dynamodb_config
    )

    print(
        "DynamoDB resource successfully created"
    )

    return dynamodb


# ============================================================
# DECIMAL JSON CONVERTER
# ============================================================

def decimal_default(obj):

    if isinstance(
        obj,
        Decimal
    ):

        return int(obj)

    raise TypeError(
        f"Object of type "
        f"{type(obj).__name__} "
        "is not JSON serializable"
    )


# ============================================================
# RESPONSE HELPER
# ============================================================

def response(
    status_code,
    body
):

    return {

        "statusCode":
            status_code,

        "headers": {

            "Content-Type":
                "application/json"

        },

        "body":
            json.dumps(
                body,
                default=decimal_default
            )
    }


# ============================================================
# MAIN LAMBDA HANDLER
# ============================================================

def lambda_handler(
    event,
    context
):

    print(
        "================================"
    )

    print(
        "=== ShiftFair Decisions ==="
    )

    print(
        "================================"
    )

    start_time = time.time()

    try:

        # ----------------------------------------------------
        # CREATE DYNAMODB RESOURCE
        # ----------------------------------------------------

        print(
            "Creating DynamoDB resource..."
        )

        connection_start = time.time()

        dynamodb = (
            get_dynamodb_resource()
        )

        print(
            "DynamoDB resource created in "
            f"{time.time() - connection_start:.2f} "
            "seconds"
        )


        # ----------------------------------------------------
        # CONNECTION TEST
        # ----------------------------------------------------

        print(
            "Creating DynamoDB client "
            "for connection test..."
        )

        client = (
            dynamodb.meta.client
        )

        print(
            "Calling DynamoDB list_tables..."
        )

        tables_response = (
            client.list_tables()
        )

        print(
            f"DynamoDB tables: "
            f"{tables_response.get('TableNames')}"
        )

        print(
            "DynamoDB connection test PASSED"
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table = dynamodb.Table(
            TABLE_NAME
        )

        print(
            f"Using table: "
            f"{TABLE_NAME}"
        )


        # ----------------------------------------------------
        # SCAN DATABASE
        # ----------------------------------------------------

        print(
            "Scanning decision records..."
        )

        scan_start = time.time()

        result = table.scan()

        items = result.get(
            "Items",
            []
        )

        print(
            f"Total records found: "
            f"{len(items)}"
        )

        print(
            "Scan completed in "
            f"{time.time() - scan_start:.2f} "
            "seconds"
        )


        # ----------------------------------------------------
        # FILTER DECISIONS
        # ----------------------------------------------------

        print(
            "Filtering decision records..."
        )

        decisions = []

        for item in items:

            if (
                item.get("sk")
                == "DECISION"
            ):

                decisions.append(
                    item
                )


        # ----------------------------------------------------
        # SORT DECISIONS
        # ----------------------------------------------------

        decisions.sort(

            key=lambda item:
                item.get(
                    "created_at",
                    0
                ),

            reverse=True
        )


        print(
            f"Found "
            f"{len(decisions)} "
            "decision(s)"
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        total_time = (
            time.time()
            - start_time
        )

        print(
            "================================"
        )

        print(
            f"TOTAL HANDLER TIME: "
            f"{total_time:.2f} seconds"
        )

        print(
            "================================"
        )


        return response(

            200,

            {

                "decision_count":
                    len(decisions),

                "decisions":
                    decisions
            }
        )


    # --------------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------------

    except (
        EndpointConnectionError,
        ConnectTimeoutError,
        ReadTimeoutError
    ) as e:

        print(
            "DynamoDB connection error:"
        )

        print(
            str(e)
        )

        return response(

            500,

            {

                "error":
                    "Could not connect "
                    "to DynamoDB",

                "details":
                    str(e)
            }
        )


    # --------------------------------------------------------
    # DYNAMODB ERROR
    # --------------------------------------------------------

    except ClientError as e:

        print(
            "DynamoDB error:"
        )

        print(
            str(e)
        )

        return response(

            500,

            {

                "error":
                    "DynamoDB error",

                "details":
                    str(e)
            }
        )


    # --------------------------------------------------------
    # UNEXPECTED ERROR
    # --------------------------------------------------------

    except Exception as e:

        print(
            "Unexpected error:"
        )

        print(
            str(e)
        )

        return response(

            500,

            {

                "error":
                    "Unexpected server error",

                "details":
                    str(e)
            }
        )