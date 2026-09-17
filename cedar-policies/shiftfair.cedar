// ShiftFair Cedar Policy Set
// Fairness and safety rules for assigning a shift to an employee.

// ============================================================
// Rule 1: Maximum weekly working hours
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.weekly_hours + resource.shift_hours >
    principal.maximum_weekly_hours
};


// ============================================================
// Rule 2: Minimum rest between shifts
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    resource.hours_since_last_shift <
    principal.minimum_rest_hours
};


// ============================================================
// Rule 3: Skill compatibility
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.skill_level <
    resource.required_skill_level
};


// ============================================================
// Rule 4: Maximum consecutive working days
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.consecutive_working_days >=
    principal.maximum_consecutive_days
};


// ============================================================
// Rule 5: Minimum notice before accepting a swap
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    resource.notice_hours <
    principal.minimum_notice_hours
};


// ============================================================
// Rule 6: Maximum previous swaps
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.previous_swap_count >=
    principal.maximum_swap_count
};


// ============================================================
// Rule 7: Minimum experience requirement
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.experience_years <
    resource.required_experience_years
};


// ============================================================
// Rule 8: Minimum performance requirement
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    principal.performance_score <
    resource.minimum_performance_score
};


// ============================================================
// Rule 9: Night-shift limit
// ============================================================

forbid (
    principal,
    action == Action::"AssignShift",
    resource
)
when {
    resource.shift_type == "night" &&
    principal.current_night_count >=
    principal.max_night_shifts_per_week
};


// ============================================================
// Rule 10: Cancel swap
// Requester or manager may cancel a swap.
// ============================================================

permit (
    principal,
    action == Action::"CancelSwap",
    resource
)
when {
    principal.id == resource.from_employee ||
    principal.role == "manager"
};


// ============================================================
// Rule 11: Swap requests can proceed to evaluation.
// Actual fairness checks are performed by the policies above.
// ============================================================

permit (
    principal,
    action == Action::"RequestSwap",
    resource
);


// ============================================================
// Rule 12: Allow assignment when no fairness/safety rule
// forbids the assignment.
// ============================================================

permit (
    principal,
    action == Action::"AssignShift",
    resource
);