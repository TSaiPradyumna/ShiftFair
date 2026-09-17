import json
import os
import uuid
import time


# ============================================================
# AWS ENVIRONMENT
# ============================================================

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

from cedar_check import authorize_assignment


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
# DYNAMODB
# ============================================================

def get_dynamodb_resource():

    print("Inside get_dynamodb_resource()")

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
            "max_attempts": 1,
            "mode": "standard"
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
# LOAD ROSTER DATA
# ============================================================

def load_roster_data(table):

    result = table.scan()

    items = result.get(
        "Items",
        []
    )

    employees = []

    shifts = []

    for item in items:

        if item.get("sk") == "PROFILE":

            employees.append(item)

        elif item.get("sk") == "DETAILS":

            shifts.append(item)

    return employees, shifts


# ============================================================
# FIND EMPLOYEE
# ============================================================

def find_employee(
    employees,
    employee_id
):

    for employee in employees:

        if (
            employee.get("employee_id")
            == employee_id
        ):

            return employee

    return None


# ============================================================
# FIND SHIFT
# ============================================================

def find_shift(
    shifts,
    shift_id
):

    for shift in shifts:

        if (
            shift.get("shift_id")
            == shift_id
        ):

            return shift

    return None


# ============================================================
# CHECK SHIFT CONFLICT
# ============================================================

def has_shift_conflict(
    employee_id,
    target_date,
    target_start,
    target_end,
    all_shifts
):

    for shift in all_shifts:

        # Ignore other employees
        if (
            shift.get("employee_id")
            != employee_id
        ):

            continue

        # Ignore different dates
        if (
            shift.get("date")
            != target_date
        ):

            continue

        existing_start = shift.get(
            "start_time"
        )

        existing_end = shift.get(
            "end_time"
        )

        # Time overlap detection
        if (
            existing_start < target_end
            and existing_end > target_start
        ):

            return True

    return False


# ============================================================
# FIND ELIGIBLE PARTNERS
# ============================================================

def find_eligible_partners(
    requesting_employee,
    requested_shift,
    employees,
    all_shifts
):

    partners = []

    requesting_id = (
        requesting_employee.get(
            "employee_id"
        )
    )

    requesting_role = (
        requesting_employee.get(
            "role"
        )
    )

    requesting_department = (
        requesting_employee.get(
            "department"
        )
    )

    target_date = (
        requested_shift.get(
            "date"
        )
    )

    target_start = (
        requested_shift.get(
            "start_time"
        )
    )

    target_end = (
        requested_shift.get(
            "end_time"
        )
    )

    print(
        f"Checking availability for "
        f"{target_date} "
        f"{target_start}-{target_end}"
    )

    for employee in employees:

        employee_id = (
            employee.get(
                "employee_id"
            )
        )

        employee_name = (
            employee.get(
                "name"
            )
        )

        # RULE 1:
        # Cannot swap with yourself

        if employee_id == requesting_id:

            print(
                f"Skipping {employee_id}: "
                "requesting employee"
            )

            continue

        # RULE 2:
        # Same role required

        if (
            employee.get("role")
            != requesting_role
        ):

            print(
                f"Skipping {employee_id}: "
                "different role"
            )

            continue

        # RULE 3:
        # Same department required

        if (
            employee.get("department")
            != requesting_department
        ):

            print(
                f"Skipping {employee_id}: "
                "different department"
            )

            continue

        # RULE 4:
        # No overlapping shift

        conflict = has_shift_conflict(
            employee_id,
            target_date,
            target_start,
            target_end,
            all_shifts
        )

        if conflict:

            print(
                f"Skipping {employee_id} "
                f"({employee_name}): "
                "shift conflict"
            )

            continue

        # EMPLOYEE IS ELIGIBLE

        print(
            f"Eligible: "
            f"{employee_id} "
            f"({employee_name})"
        )

        partners.append(employee)

    return partners


# ============================================================
# SELECT BEST PARTNER
# ============================================================

def select_best_partner(
    partners
):

    if not partners:

        return None

    # Current hackathon algorithm:
    # Select first eligible employee

    return partners[0]


# ============================================================
# CREATE EXPLANATION
# ============================================================

def create_explanation(
    requesting_employee,
    requested_shift,
    selected_partner,
    reason_text,
    eligible_count
):

    partner_id = selected_partner.get(
        "employee_id"
    )

    partner_name = selected_partner.get(
        "name"
    )

    role = requesting_employee.get(
        "role"
    )

    department = requesting_employee.get(
        "department"
    )

    date = requested_shift.get(
        "date"
    )

    start_time = requested_shift.get(
        "start_time"
    )

    end_time = requested_shift.get(
        "end_time"
    )

    explanation = (

        f"{partner_name} ({partner_id}) "
        "was selected as the suggested "
        "swap partner. "

        f"They have the same role "
        f"({role}) and work in the "
        f"same department "
        f"({department}). "

        f"They have no conflicting "
        f"shift on {date} between "
        f"{start_time} and {end_time}. "

        f"{eligible_count} eligible "
        "partner(s) were found. "

        f"Request reason: "
        f"{reason_text or 'No reason provided'}."
    )

    return explanation


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
        "=== ShiftFair Swap Request ==="
    )

    print(
        "================================"
    )

    start_time = time.time()


    # --------------------------------------------------------
    # PARSE REQUEST
    # --------------------------------------------------------

    try:

        body = json.loads(
            event.get("body") or "{}"
        )

    except json.JSONDecodeError:

        return _response(
            400,
            {
                "error":
                    "Invalid JSON request body"
            }
        )


    from_employee = body.get(
        "from_employee"
    )

    shift_id = body.get(
        "shift_id"
    )

    reason_text = body.get(
        "reason_text",
        ""
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not from_employee:

        return _response(
            400,
            {
                "error":
                    "from_employee is required"
            }
        )


    if not shift_id:

        return _response(
            400,
            {
                "error":
                    "shift_id is required"
            }
        )


    print(
        f"Employee: "
        f"{from_employee}"
    )

    print(
        f"Shift: "
        f"{shift_id}"
    )

    print(
        f"Reason: "
        f"{reason_text}"
    )


    # --------------------------------------------------------
    # REQUEST ID
    # --------------------------------------------------------

    request_id = str(
        uuid.uuid4()
    )[:8]


    # --------------------------------------------------------
    # DYNAMODB OPERATIONS
    #
    # We load the roster BEFORE Cedar because Cedar must
    # authorize using the actual employee and shift data.
    # --------------------------------------------------------

    try:

        print(
            "Creating DynamoDB resource..."
        )

        connection_start = time.time()


        # ----------------------------------------------------
        # CREATE RESOURCE
        # ----------------------------------------------------

        dynamodb = (
            get_dynamodb_resource()
        )


        print(
            "DynamoDB resource created in "
            f"{time.time() - connection_start:.2f} "
            "seconds"
        )


        # ----------------------------------------------------
        # DYNAMODB CONNECTION TEST
        # ----------------------------------------------------

        print(
            "Creating DynamoDB client for "
            "connection test..."
        )

        client = dynamodb.meta.client


        print(
            "Calling DynamoDB list_tables..."
        )

        tables_response = client.list_tables()


        print(
            f"DynamoDB tables: "
            f"{tables_response.get('TableNames')}"
        )


        print(
            "DynamoDB connection test PASSED"
        )


        # ----------------------------------------------------
        # GET TABLE
        # ----------------------------------------------------

        table = dynamodb.Table(
            TABLE_NAME
        )


        print(
            f"Using table: {TABLE_NAME}"
        )


        # ----------------------------------------------------
        # LOAD ALL ROSTER DATA
        # ----------------------------------------------------

        print(
            "Loading roster data..."
        )

        scan_start = time.time()


        employees, shifts = (
            load_roster_data(table)
        )


        print(
            f"Found "
            f"{len(employees)} employees"
        )

        print(
            f"Found "
            f"{len(shifts)} shifts"
        )

        print(
            "Roster loaded in "
            f"{time.time() - scan_start:.2f} "
            "seconds"
        )


        # ----------------------------------------------------
        # FIND REQUESTING EMPLOYEE
        # ----------------------------------------------------

        requesting_employee = (
            find_employee(
                employees,
                from_employee
            )
        )


        if not requesting_employee:

            return _response(
                404,
                {
                    "error":
                        f"Employee "
                        f"{from_employee} "
                        "was not found"
                }
            )


        # ----------------------------------------------------
        # FIND REQUESTED SHIFT
        # ----------------------------------------------------

        requested_shift = (
            find_shift(
                shifts,
                shift_id
            )
        )


        if not requested_shift:

            return _response(
                404,
                {
                    "error":
                        f"Shift "
                        f"{shift_id} "
                        "was not found"
                }
            )


        # ----------------------------------------------------
        # VERIFY SHIFT OWNERSHIP
        # ----------------------------------------------------

        shift_owner = (
            requested_shift.get(
                "employee_id"
            )
        )


        if shift_owner != from_employee:

            return _response(
                400,
                {
                    "error":
                        "The specified employee "
                        "does not own this shift",

                    "shift_owner":
                        shift_owner
                }
            )


        # ----------------------------------------------------
        # CEDAR AUTHORIZATION
        # ----------------------------------------------------

        print(
            "Running Cedar authorization..."
        )

        cedar_start = time.time()


        cedar_result = (
            authorize_assignment(
                requesting_employee,
                requested_shift,
                employees
            )
        )


        print(
            "Cedar authorization completed "
            f"in {time.time() - cedar_start:.2f} "
            "seconds"
        )


        cedar_allowed = cedar_result.get(
            "allowed",
            False
        )

        cedar_reason = cedar_result.get(
            "reason",
            "Cedar authorization denied."
        )


        # ----------------------------------------------------
        # CEDAR DENIAL
        # ----------------------------------------------------

        if not cedar_allowed:

            print(
                "================================"
            )

            print(
                "CEDAR DENIED THE REQUEST"
            )

            print(
                "================================"
            )


            return _response(
                403,
                {
                    "request_id":
                        request_id,

                    "status":
                        "denied",

                    "reason":
                        cedar_reason,

                    "cedar_decision":
                        cedar_result.get(
                            "decision"
                        )
                }
            )


        # ----------------------------------------------------
        # CEDAR APPROVED
        # ----------------------------------------------------

        print(
            "================================"
        )

        print(
            "CEDAR APPROVED THE REQUEST"
        )

        print(
            "================================"
        )


        # ----------------------------------------------------
        # FIND ELIGIBLE PARTNERS
        # ----------------------------------------------------

        print(
            "Finding eligible partners..."
        )

        matching_start = time.time()


        partners = (
            find_eligible_partners(
                requesting_employee,
                requested_shift,
                employees,
                shifts
            )
        )


        print(
            "Partner matching completed in "
            f"{time.time() - matching_start:.2f} "
            "seconds"
        )

        print(
            f"Total eligible partners: "
            f"{len(partners)}"
        )


        # ----------------------------------------------------
        # NO PARTNER FOUND
        # ----------------------------------------------------

        if not partners:

            explanation = (

                "No eligible swap partner "
                "was found. Employees with "
                "the same role and department "
                "were either unavailable or "
                "had conflicting shifts."
            )


            decision_item = {

                "pk":
                    f"REQUEST#{request_id}",

                "sk":
                    "DECISION",

                "request_id":
                    request_id,

                "from_employee":
                    from_employee,

                "shift_id":
                    shift_id,

                "reason_text":
                    reason_text,

                "status":
                    "no_partner_found",

                "eligible_partner_count":
                    0,

                "cedar_decision":
                    "ALLOW",

                "cedar_reason":
                    cedar_reason,

                "explanation":
                    explanation,

                "created_at":
                    int(time.time())
            }


            table.put_item(
                Item=decision_item
            )


            return _response(
                200,
                {
                    "request_id":
                        request_id,

                    "status":
                        "no_partner_found",

                    "suggested_partner":
                        None,

                    "eligible_partner_count":
                        0,

                    "cedar_decision":
                        "ALLOW",

                    "explanation":
                        explanation
                }
            )


        # ----------------------------------------------------
        # SELECT PARTNER
        # ----------------------------------------------------

        selected_partner = (
            select_best_partner(
                partners
            )
        )


        suggested_partner = (
            selected_partner.get(
                "employee_id"
            )
        )


        suggested_partner_name = (
            selected_partner.get(
                "name"
            )
        )


        # ----------------------------------------------------
        # CREATE EXPLANATION
        # ----------------------------------------------------

        explanation = (
            create_explanation(
                requesting_employee,
                requested_shift,
                selected_partner,
                reason_text,
                len(partners)
            )
        )


        # ----------------------------------------------------
        # SAVE DECISION
        # ----------------------------------------------------

        print(
            "Saving decision..."
        )

        save_start = time.time()


        decision_item = {

            "pk":
                f"REQUEST#{request_id}",

            "sk":
                "DECISION",

            "request_id":
                request_id,

            "from_employee":
                from_employee,

            "shift_id":
                shift_id,

            "reason_text":
                reason_text,

            "suggested_partner":
                suggested_partner,

            "suggested_partner_name":
                suggested_partner_name,

            "status":
                "pending_approval",

            "eligible_partner_count":
                len(partners),

            "cedar_decision":
                "ALLOW",

            "cedar_reason":
                cedar_reason,

            "explanation":
                explanation,

            "created_at":
                int(time.time())
        }


        table.put_item(
            Item=decision_item
        )


        print(
            "Decision saved in "
            f"{time.time() - save_start:.2f} "
            "seconds"
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


        return _response(
            500,
            {
                "error":
                    "Could not connect to DynamoDB",

                "details":
                    str(e)
            }
        )


    # --------------------------------------------------------
    # AWS ERROR
    # --------------------------------------------------------

    except ClientError as e:

        print(
            "DynamoDB error:"
        )

        print(
            str(e)
        )


        return _response(
            500,
            {
                "error":
                    "DynamoDB error",

                "details":
                    str(e)
            }
        )


    # --------------------------------------------------------
    # CEDAR / POLICY ERROR
    # --------------------------------------------------------

    except FileNotFoundError as e:

        print(
            "Cedar policy file error:"
        )

        print(
            str(e)
        )


        return _response(
            500,
            {
                "error":
                    "Cedar policy configuration error",

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


        return _response(
            500,
            {
                "error":
                    "Unexpected server error",

                "details":
                    str(e)
            }
        )


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    total_time = (
        time.time() - start_time
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


    return _response(
        200,
        {
            "request_id":
                request_id,

            "status":
                "pending_approval",

            "suggested_partner":
                suggested_partner,

            "suggested_partner_name":
                suggested_partner_name,

            "eligible_partner_count":
                len(partners),

            "cedar_decision":
                "ALLOW",

            "explanation":
                explanation
        }
    )


# ============================================================
# RESPONSE HELPER
# ============================================================

def _response(
    status_code,
    body_dict
):

    return {

        "statusCode":
            status_code,

        "headers": {

            "Content-Type":
                "application/json",

            "Access-Control-Allow-Origin":
                "http://127.0.0.1:5500",

            "Access-Control-Allow-Headers":
                "Content-Type",

            "Access-Control-Allow-Methods":
                "GET,POST,OPTIONS"
        },

        "body":
            json.dumps(body_dict)
    }
