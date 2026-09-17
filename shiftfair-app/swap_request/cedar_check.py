import json
import os

from cedarpy import is_authorized, Decision


# ============================================================
# CEDAR POLICY LOCATION
# ============================================================

# The Cedar policy files are packaged into a Lambda layer.
# Locally, SAM mounts the layer under /opt.
CEDAR_POLICY_PATH = os.environ.get(
    "CEDAR_POLICY_PATH",
    "/opt/shiftfair.cedar"
)


# ============================================================
# LOAD CEDAR POLICY
# ============================================================

def load_cedar_policy():

    print(
        f"Loading Cedar policy from: "
        f"{CEDAR_POLICY_PATH}"
    )

    if not os.path.exists(CEDAR_POLICY_PATH):

        raise FileNotFoundError(
            f"Cedar policy file not found: "
            f"{CEDAR_POLICY_PATH}"
        )

    with open(
        CEDAR_POLICY_PATH,
        "r",
        encoding="utf-8"
    ) as policy_file:

        policy = policy_file.read()

    print(
        f"Cedar policy loaded "
        f"({len(policy)} characters)"
    )

    return policy


# ============================================================
# CONVERT EMPLOYEE TO CEDAR ENTITY
# ============================================================

def employee_to_cedar_entity(employee):

    employee_id = employee.get(
        "employee_id"
    )

    return {
        "uid": {
            "type": "User",
            "id": employee_id
        },

        "attrs": {
            "id": employee_id,

            # Cedar policy values
            "role": employee.get(
                "role",
                "nurse"
            ).lower(),

            "department": employee.get(
                "department",
                "Emergency"
            ),

            "weekly_hours": int(
                employee.get(
                    "weekly_hours",
                    0
                )
            ),

            "maximum_weekly_hours": int(
                employee.get(
                    "maximum_weekly_hours",
                    48
                )
            ),

            "skill_level": int(
                employee.get(
                    "skill_level",
                    0
                )
            ),

            "consecutive_working_days": int(
                employee.get(
                    "consecutive_working_days",
                    0
                )
            ),

            "maximum_consecutive_days": int(
                employee.get(
                    "maximum_consecutive_days",
                    5
                )
            ),

            "minimum_notice_hours": int(
                employee.get(
                    "minimum_notice_hours",
                    12
                )
            ),

            "previous_swap_count": int(
                employee.get(
                    "previous_swap_count",
                    0
                )
            ),

            "maximum_swap_count": int(
                employee.get(
                    "maximum_swap_count",
                    3
                )
            ),

            "experience_years": int(
                employee.get(
                    "experience_years",
                    0
                )
            ),

            "performance_score": int(
                employee.get(
                    "performance_score",
                    0
                )
            ),

            "current_night_count": int(
                employee.get(
                    "current_night_count",
                    0
                )
            ),

            "max_night_shifts_per_week": int(
                employee.get(
                    "max_night_shifts_per_week",
                    3
                )
            ),

            "minimum_rest_hours": int(
                employee.get(
                    "minimum_rest_hours",
                    10
                )
            )
        },

        "parents": []
    }


# ============================================================
# CONVERT SHIFT TO CEDAR ENTITY
# ============================================================

def shift_to_cedar_entity(shift):

    shift_id = shift.get(
        "shift_id"
    )

    return {
        "uid": {
            "type": "Shift",
            "id": shift_id
        },

        "attrs": {
            "shift_type": shift.get(
                "shift_type",
                "day"
            ),

            "shift_hours": int(
                shift.get(
                    "shift_hours",
                    8
                )
            ),

            "hours_since_last_shift": int(
                shift.get(
                    "hours_since_last_shift",
                    24
                )
            ),

            "required_skill_level": int(
                shift.get(
                    "required_skill_level",
                    0
                )
            ),

            "notice_hours": int(
                shift.get(
                    "notice_hours",
                    24
                )
            ),

            "required_experience_years": int(
                shift.get(
                    "required_experience_years",
                    0
                )
            ),

            "minimum_performance_score": int(
                shift.get(
                    "minimum_performance_score",
                    0
                )
            ),

            "from_employee": shift.get(
                "employee_id"
            )
        },

        "parents": []
    }


# ============================================================
# AUTHORIZE SHIFT ASSIGNMENT
# ============================================================

def authorize_assignment(
    employee,
    shift,
    all_employees=None
):

    print(
        "================================"
    )

    print(
        "=== Cedar Authorization ==="
    )

    print(
        f"Principal: "
        f"{employee.get('employee_id')}"
    )

    print(
        f"Resource: "
        f"{shift.get('shift_id')}"
    )

    # --------------------------------------------------------
    # LOAD POLICY
    # --------------------------------------------------------

    policies = load_cedar_policy()

    # --------------------------------------------------------
    # BUILD ENTITIES
    # --------------------------------------------------------

    entities = []

    if all_employees:

        for roster_employee in all_employees:

            entities.append(
                employee_to_cedar_entity(
                    roster_employee
                )
            )

    else:

        entities.append(
            employee_to_cedar_entity(
                employee
            )
        )

    entities.append(
        shift_to_cedar_entity(
            shift
        )
    )

    # --------------------------------------------------------
    # BUILD REQUEST
    # --------------------------------------------------------

    employee_id = employee.get(
        "employee_id"
    )

    shift_id = shift.get(
        "shift_id"
    )

    request = {

        "principal":
            f'User::"{employee_id}"',

        "action":
            'Action::"AssignShift"',

        "resource":
            f'Shift::"{shift_id}"',

        "context": {}
    }

    print(
        "Cedar request:"
    )

    print(
        json.dumps(
            request,
            indent=2
        )
    )

    # --------------------------------------------------------
    # CEDAR AUTHORIZATION
    # --------------------------------------------------------

    try:

        result = is_authorized(
            request,
            policies,
            entities
        )

    except Exception as e:

        print(
            "Cedar authorization error:"
        )

        print(
            str(e)
        )

        raise

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    allowed = (
        result.decision == Decision.Allow
    )

    if allowed:

        reason = (
            "Cedar authorization "
            "approved the assignment."
        )

        print(
            "Cedar decision: ALLOW"
        )

    else:

        reason = (
            "Cedar authorization "
            "denied the assignment because "
            "one or more fairness or safety "
            "policies were violated."
        )

        print(
            "Cedar decision: DENY"
        )

    print(
        "================================"
    )

    return {
        "allowed": allowed,
        "reason": reason,
        "decision": str(
            result.decision
        )
    }
