// ShiftFair Cedar Policy Set
// Rule 1: Cap night shifts per employee per week
forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    resource.shift_type == "night" &&
    principal.current_night_count >= principal.max_night_shifts_per_week
};

// Rule 2: Minimum 10 hours rest between shifts
forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    resource.hours_since_last_shift < 10
};

// Rule 3: Only the requester themself or a manager can cancel a swap request
permit (
    principal,
    action == Action::"CancelSwap",
    resource
)
when {
    principal.id == resource.from_employee || principal.role == "manager"
};

// Rule 4: Default - allow a swap to proceed to Strands evaluation if not blocked above
permit (
    principal,
    action == Action::"RequestSwap",
    resource
);
