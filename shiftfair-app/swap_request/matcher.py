import os
import boto3


DYNAMO_ENDPOINT = os.environ.get(
    "DYNAMO_ENDPOINT",
    "http://host.docker.internal:4566"
)

TABLE_NAME = os.environ.get(
    "TABLE_NAME",
    "ShiftFairTable"
)


def get_table():

    dynamodb = boto3.resource(

        "dynamodb",

        endpoint_url=DYNAMO_ENDPOINT,

        region_name="us-east-1",

        aws_access_key_id="test",

        aws_secret_access_key="test"

    )

    return dynamodb.Table(TABLE_NAME)


def get_all_data():

    table = get_table()

    result = table.scan()

    items = result.get("Items", [])

    employees = [

        item

        for item in items

        if item.get("sk") == "PROFILE"

    ]

    shifts = [

        item

        for item in items

        if item.get("sk") == "DETAILS"

    ]

    return employees, shifts


def find_employee(employee_id, employees):

    for employee in employees:

        if employee.get("employee_id") == employee_id:

            return employee

    return None


def find_shift(shift_id, shifts):

    for shift in shifts:

        if shift.get("shift_id") == shift_id:

            return shift

    return None


def get_employee_shifts(employee_id, shifts):

    return [

        shift

        for shift in shifts

        if shift.get("employee_id") == employee_id

    ]


def has_shift_conflict(candidate_id, requested_shift, shifts):

    candidate_shifts = get_employee_shifts(
        candidate_id,
        shifts
    )

    requested_date = requested_shift.get("date")

    requested_start = requested_shift.get("start_time")

    requested_end = requested_shift.get("end_time")

    for shift in candidate_shifts:

        if shift.get("date") != requested_date:

            continue

        start = shift.get("start_time")

        end = shift.get("end_time")

        if (
            requested_start < end
            and requested_end > start
        ):

            return True

    return False


def calculate_workload(employee_id, shifts):

    employee_shifts = get_employee_shifts(
        employee_id,
        shifts
    )

    return len(employee_shifts)


def calculate_score(

    candidate,
    requester,
    requested_shift,
    shifts

):

    score = 0

    candidate_id = candidate.get(
        "employee_id"
    )

    # Same role

    if (

        candidate.get("role")
        ==
        requester.get("role")

    ):

        score += 40

    # Same department

    if (

        candidate.get("department")
        ==
        requester.get("department")

    ):

        score += 30

    # No conflict

    conflict = has_shift_conflict(

        candidate_id,

        requested_shift,

        shifts

    )

    if not conflict:

        score += 20

    # Workload fairness

    workload = calculate_workload(

        candidate_id,

        shifts

    )

    workload_score = max(

        0,

        10 - workload

    )

    score += workload_score

    return {

        "score": score,

        "workload": workload,

        "has_conflict": conflict

    }


def find_eligible_partners(

    from_employee,

    shift_id

):

    employees, shifts = get_all_data()

    requester = find_employee(

        from_employee,

        employees

    )

    if not requester:

        return {

            "error":

            f"Employee {from_employee} "
            f"not found"

        }

    requested_shift = find_shift(

        shift_id,

        shifts

    )

    if not requested_shift:

        return {

            "error":

            f"Shift {shift_id} "
            f"not found"

        }

    # Verify shift ownership

    if (

        requested_shift.get(
            "employee_id"
        )

        !=

        from_employee

    ):

        return {

            "error":

            f"Shift {shift_id} "
            f"does not belong to "
            f"{from_employee}"

        }

    candidates = []

    for candidate in employees:

        candidate_id = candidate.get(
            "employee_id"
        )

        # Cannot swap with self

        if candidate_id == from_employee:

            continue

        # Must have same role

        if (

            candidate.get("role")

            !=

            requester.get("role")

        ):

            continue

        # Must have same department

        if (

            candidate.get("department")

            !=

            requester.get(
                "department"
            )

        ):

            continue

        score_data = calculate_score(

            candidate,

            requester,

            requested_shift,

            shifts

        )

        # Exclude conflicting candidates

        if score_data["has_conflict"]:

            continue

        candidates.append({

            "employee_id":

                candidate_id,

            "name":

                candidate.get("name"),

            "role":

                candidate.get("role"),

            "department":

                candidate.get(
                    "department"
                ),

            "fairness_score":

                score_data["score"],

            "current_workload":

                score_data["workload"]

        })

    candidates.sort(

        key=lambda x:

        (
            -x["fairness_score"],

            x["current_workload"],

            x["employee_id"]
        )

    )

    return {

        "requester":

            requester,

        "requested_shift":

            requested_shift,

        "eligible_partners":

            candidates

    }