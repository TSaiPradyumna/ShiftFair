/* =========================================================
   SHIFTFAIR FRONTEND
   ========================================================= */


/* =========================================================
   API CONFIGURATION
   ========================================================= */

/*
 * IMPORTANT:
 *
 * The backend is currently running through:
 *
 * http://127.0.0.1:3000
 *
 * Do NOT rename this to API_BASE.
 */

const API_URL = "http://127.0.0.1:3000";


/*
 * Actual backend roster structure:
 *
 * {
 *     employee_count: 4,
 *     shift_count: 4,
 *     roster: [
 *         {
 *             employee_id: "E001",
 *             name: "Alice Johnson",
 *             role: "Nurse",
 *             department: "Emergency",
 *             shifts: [...]
 *         }
 *     ]
 * }
 */

let rosterData = [];


/* =========================================================
   UTILITY HELPERS
   ========================================================= */

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function getDecisionClass(decision) {

    const value =
        String(decision || "")
            .toUpperCase();

    return (
        value === "ALLOW" ||
        value === "ALLOWED"
    )
        ? "allowed"
        : "denied";
}


function formatDecision(decision) {

    if (!decision) {
        return "UNKNOWN";
    }

    return String(decision)
        .toUpperCase();
}


/* =========================================================
   ANIMATED COUNTERS
   ========================================================= */

function animateCounter(
    elementId,
    targetValue
) {

    const el =
        document.getElementById(
            elementId
        );

    if (!el) {
        return;
    }

    const target =
        parseInt(
            targetValue,
            10
        );

    if (isNaN(target)) {

        el.textContent =
            targetValue;

        return;
    }

    let current = 0;

    const duration = 900;

    const stepTime =
        Math.max(
            Math.floor(
                duration /
                Math.max(
                    target,
                    1
                )
            ),
            20
        );


    const timer =
        setInterval(
            () => {

                current +=
                    Math.ceil(
                        target /
                        (
                            duration /
                            stepTime
                        )
                    );


                if (
                    current >=
                    target
                ) {

                    el.textContent =
                        target;

                    clearInterval(
                        timer
                    );

                } else {

                    el.textContent =
                        current;
                }

            },
            stepTime
        );
}


/* =========================================================
   SCROLL REVEAL
   ========================================================= */

function initScrollReveal() {

    const revealEls =
        document.querySelectorAll(
            ".reveal"
        );


    if (
        !(
            "IntersectionObserver"
            in window
        ) ||
        revealEls.length === 0
    ) {

        revealEls.forEach(
            el => {

                el.classList.add(
                    "in-view"
                );

            }
        );

        return;
    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(
                    entry => {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "in-view"
                            );

                            observer.unobserve(
                                entry.target
                            );
                        }

                    }
                );

            },
            {
                threshold: 0.15
            }
        );


    revealEls.forEach(
        el => {

            observer.observe(
                el
            );

        }
    );
}


/* =========================================================
   LOAD ROSTER
   ========================================================= */

async function loadRoster() {

    try {

        console.log(
            "Loading ShiftFair roster..."
        );


        const response =
            await fetch(
                `${API_URL}/roster`
            );


        if (!response.ok) {

            throw new Error(
                `Roster request failed: HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Roster API response:",
            data
        );


        /*
         * THIS IS THE IMPORTANT PART.
         *
         * The real backend returns:
         *
         * data.roster
         *
         * NOT:
         *
         * data.employees
         * data.shifts
         */

        rosterData =
            Array.isArray(
                data.roster
            )
                ? data.roster
                : [];


        console.log(
            "Loaded employees:",
            rosterData
        );


        /*
         * Update statistics.
         */

        updateRosterStats();


        /*
         * Populate employee dropdown.
         */

        populateEmployeeDropdown();


        /*
         * Populate the selected employee's
         * shifts.
         */

        populateShiftDropdown();


        /*
         * Display roster cards.
         */

        displayRoster(
            rosterData
        );


    } catch (error) {

        console.error(
            "Failed to load roster:",
            error
        );


        rosterData = [];


        const employeeCount =
            document.getElementById(
                "employeeCount"
            );


        const shiftCount =
            document.getElementById(
                "shiftCount"
            );


        if (employeeCount) {

            employeeCount.textContent =
                "—";
        }


        if (shiftCount) {

            shiftCount.textContent =
                "—";
        }


        const roster =
            document.getElementById(
                "rosterGrid"
            );


        if (roster) {

            roster.innerHTML = `

                <div class="empty-state">

                    Unable to load roster.

                    <br><br>

                    Make sure the ShiftFair API
                    is running on port 3000.

                </div>

            `;
        }


        const employeeSelect =
            document.getElementById(
                "employeeSelect"
            );


        const shiftSelect =
            document.getElementById(
                "shiftSelect"
            );


        if (employeeSelect) {

            employeeSelect.innerHTML = `

                <option value="">

                    Unable to load employees

                </option>

            `;
        }


        if (shiftSelect) {

            shiftSelect.innerHTML = `

                <option value="">

                    Unable to load shifts

                </option>

            `;
        }
    }
}


/* =========================================================
   UPDATE ROSTER STATISTICS
   ========================================================= */

function updateRosterStats() {

    const employeeCount =
        document.getElementById(
            "employeeCount"
        );


    const shiftCount =
        document.getElementById(
            "shiftCount"
        );


    const totalEmployees =
        rosterData.length;


    const totalShifts =
        rosterData.reduce(
            (
                total,
                employee
            ) => {

                const shifts =
                    Array.isArray(
                        employee.shifts
                    )
                        ? employee.shifts
                        : [];


                return (
                    total +
                    shifts.length
                );

            },
            0
        );


    if (employeeCount) {

        employeeCount.textContent =
            "0";


        animateCounter(
            "employeeCount",
            totalEmployees
        );
    }


    if (shiftCount) {

        shiftCount.textContent =
            "0";


        animateCounter(
            "shiftCount",
            totalShifts
        );
    }
}


/* =========================================================
   LOAD DECISIONS
   ========================================================= */

async function loadDecisions() {

    try {

        console.log(
            "Loading arbitration decisions..."
        );


        const response =
            await fetch(
                `${API_URL}/decisions`
            );


        if (!response.ok) {

            throw new Error(
                `Decision request failed: HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Decision API response:",
            data
        );


        const decisions =
            Array.isArray(
                data.decisions
            )
                ? data.decisions
                : [];


        const decisionCount =
            document.getElementById(
                "decisionCount"
            );


        if (decisionCount) {

            decisionCount.textContent =
                "0";


            animateCounter(
                "decisionCount",
                decisions.length
            );
        }


        displayDecisions(
            decisions
        );


    } catch (error) {

        console.error(
            "Failed to load decisions:",
            error
        );


        const decisionCount =
            document.getElementById(
                "decisionCount"
            );


        if (decisionCount) {

            decisionCount.textContent =
                "—";
        }


        const decisionsElement =
            document.getElementById(
                "decisions"
            );


        if (decisionsElement) {

            decisionsElement.innerHTML = `

                <div class="empty-state">

                    Unable to load decision history.

                </div>

            `;
        }
    }
}


/* =========================================================
   EMPLOYEE DROPDOWN
   ========================================================= */

function populateEmployeeDropdown() {

    const select =
        document.getElementById(
            "employeeSelect"
        );


    if (!select) {
        return;
    }


    select.innerHTML = "";


    if (
        rosterData.length === 0
    ) {

        select.innerHTML = `

            <option value="">

                No employees available

            </option>

        `;

        return;
    }


    rosterData.forEach(
        employee => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                employee.employee_id;


            option.textContent =
                `${employee.name} (${employee.employee_id})`;


            select.appendChild(
                option
            );

        }
    );


    /*
     * Because the browser selects the first
     * option automatically, this will select
     * the first employee and allow
     * populateShiftDropdown() to immediately
     * show their shift.
     */
}


/* =========================================================
   SHIFT DROPDOWN
   ========================================================= */

function populateShiftDropdown() {

    const select =
        document.getElementById(
            "shiftSelect"
        );


    const employeeSelect =
        document.getElementById(
            "employeeSelect"
        );


    if (
        !select ||
        !employeeSelect
    ) {
        return;
    }


    const selectedEmployeeId =
        employeeSelect.value;


    select.innerHTML = "";


    /*
     * Find the selected employee.
     */

    const selectedEmployee =
        rosterData.find(
            employee =>
                employee.employee_id ===
                selectedEmployeeId
        );


    if (!selectedEmployee) {

        select.innerHTML = `

            <option value="">

                Select employee first

            </option>

        `;

        return;
    }


    /*
     * The shifts are inside:
     *
     * selectedEmployee.shifts
     */

    const shifts =
        Array.isArray(
            selectedEmployee.shifts
        )
            ? selectedEmployee.shifts
            : [];


    if (
        shifts.length === 0
    ) {

        select.innerHTML = `

            <option value="">

                No shifts available

            </option>

        `;

        return;
    }


    /*
     * Add every shift for the
     * selected employee.
     */

    shifts.forEach(
        shift => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                shift.shift_id;


            option.textContent =
                `${shift.shift_id} — ${shift.date} (${shift.start_time} - ${shift.end_time})`;


            select.appendChild(
                option
            );

        }
    );


    console.log(
        `Loaded ${shifts.length} shift(s) for ${selectedEmployeeId}`
    );
}


/* =========================================================
   DISPLAY ROSTER
   ========================================================= */

function displayRoster(
    roster
) {

    const container =
        document.getElementById(
            "rosterGrid"
        );


    if (!container) {
        return;
    }


    if (
        !roster ||
        roster.length === 0
    ) {

        container.innerHTML = `

            <div class="empty-state">

                No employees found in the roster.

            </div>

        `;

        return;
    }


    container.innerHTML =
        roster.map(
            employee => {

                const shifts =
                    Array.isArray(
                        employee.shifts
                    )
                        ? employee.shifts
                        : [];


                const shiftHTML =
                    shifts.length > 0

                        ? shifts.map(
                            shift => `

                                <div class="shift-item">

                                    <div class="shift-title">

                                        ${escapeHTML(
                                            shift.shift_id
                                        )}

                                        ·

                                        ${escapeHTML(
                                            shift.shift_type ||
                                            "Shift"
                                        )}

                                    </div>


                                    <div class="shift-meta">

                                        ${escapeHTML(
                                            shift.date
                                        )}

                                        ·

                                        ${escapeHTML(
                                            shift.start_time
                                        )}

                                        -

                                        ${escapeHTML(
                                            shift.end_time
                                        )}

                                    </div>

                                </div>

                            `
                        ).join("")

                        : `

                            <div class="empty-state">

                                No shifts assigned.

                            </div>

                        `;


                return `

                    <article class="roster-card">


                        <div class="roster-header">

                            <div>

                                <div class="roster-name">

                                    ${escapeHTML(
                                        employee.name
                                    )}

                                </div>


                                <div class="roster-id">

                                    ${escapeHTML(
                                        employee.employee_id
                                    )}

                                </div>

                            </div>


                            <div class="roster-role">

                                ${escapeHTML(
                                    employee.role
                                )}

                            </div>

                        </div>


                        <div class="roster-info">


                            <div class="roster-info-item">

                                <div class="roster-info-label">

                                    Department

                                </div>


                                <div class="roster-info-value">

                                    ${escapeHTML(
                                        employee.department
                                    )}

                                </div>

                            </div>


                            <div class="roster-info-item">

                                <div class="roster-info-label">

                                    Weekly Hours

                                </div>


                                <div class="roster-info-value">

                                    ${escapeHTML(
                                        employee.weekly_hours
                                    )}

                                    h /

                                    ${escapeHTML(
                                        employee.maximum_weekly_hours
                                    )}

                                    h

                                </div>

                            </div>


                            <div class="roster-info-item">

                                <div class="roster-info-label">

                                    Skill Level

                                </div>


                                <div class="roster-info-value">

                                    ${escapeHTML(
                                        employee.skill_level
                                    )}

                                </div>

                            </div>


                            <div class="roster-info-item">

                                <div class="roster-info-label">

                                    Experience

                                </div>


                                <div class="roster-info-value">

                                    ${escapeHTML(
                                        employee.experience_years
                                    )}

                                    years

                                </div>

                            </div>


                        </div>


                        <div class="shift-list">

                            ${shiftHTML}

                        </div>


                    </article>

                `;

            }
        ).join("");
}


/* =========================================================
   DISPLAY ARBITRATION RESULT
   ========================================================= */

function displayResult(
    result
) {

    const section =
        document.getElementById(
            "resultSection"
        );


    const card =
        document.getElementById(
            "resultCard"
        );


    if (
        !section ||
        !card
    ) {
        return;
    }


    section.classList.remove(
        "hidden"
    );


    const cedarDecision =
        formatDecision(
            result.cedar_decision ||
            result.decision
        );


    const decisionClass =
        getDecisionClass(
            cedarDecision
        );


    const isAllowed =
        decisionClass ===
        "allowed";


    const status =
        result.status ||
        (
            isAllowed
                ? "approved"
                : "denied"
        );


    const reason =
        result.reason ||
        result.cedar_reason ||
        "";


    const explanation =
        result.explanation ||
        reason ||
        (
            isAllowed
                ? "The request passed the ShiftFair arbitration checks."
                : "The request was denied by the ShiftFair arbitration policy."
        );


    const suggestedPartner =
        result.suggested_partner_name ||
        result.suggested_partner ||
        "None";


    const eligibleCount =
        result.eligible_partner_count !== undefined
            ? result.eligible_partner_count
            : "—";


    card.className =
        `result-card ${
            isAllowed
                ? ""
                : "denied"
        }`;


    card.innerHTML = `

        <div class="result-top">

            <div>

                <div class="section-eyebrow">

                    CEDAR AUTHORIZATION

                </div>


                <h3 style="
                    margin-top: 8px;
                    font-size: 24px;
                ">

                    ${
                        isAllowed
                            ? "Request authorized"
                            : "Request denied"
                    }

                </h3>

            </div>


            <div class="result-status">

                ${
                    isAllowed
                        ? "✓"
                        : "✕"
                }

                ${escapeHTML(
                    cedarDecision
                )}

            </div>

        </div>


        <div class="result-grid">


            <div class="result-item">

                <div class="result-item-label">

                    Request ID

                </div>


                <div class="result-item-value">

                    ${escapeHTML(
                        result.request_id ||
                        "—"
                    )}

                </div>

            </div>


            <div class="result-item">

                <div class="result-item-label">

                    Status

                </div>


                <div class="result-item-value">

                    ${escapeHTML(
                        status
                    )}

                </div>

            </div>


            <div class="result-item">

                <div class="result-item-label">

                    Suggested Partner

                </div>


                <div class="result-item-value">

                    ${escapeHTML(
                        suggestedPartner
                    )}

                </div>

            </div>


            <div class="result-item">

                <div class="result-item-label">

                    Eligible Partners

                </div>


                <div class="result-item-value">

                    ${escapeHTML(
                        eligibleCount
                    )}

                </div>

            </div>


        </div>


        <div class="result-explanation">

            <strong>

                Arbitration explanation

            </strong>


            <br><br>


            ${escapeHTML(
                explanation
            )}

        </div>


        ${
            reason &&
            !isAllowed

                ? `

                    <div class="result-reason">

                        Policy reason:

                        ${escapeHTML(
                            reason
                        )}

                    </div>

                `

                : ""
        }

    `;


    section.scrollIntoView({

        behavior:
            "smooth",

        block:
            "start"

    });
}


/* =========================================================
   DISPLAY DECISION HISTORY
   ========================================================= */

function displayDecisions(
    decisions
) {

    const container =
        document.getElementById(
            "decisions"
        );


    if (!container) {
        return;
    }


    if (
        !decisions ||
        decisions.length === 0
    ) {

        container.innerHTML = `

            <div class="empty-state">

                No arbitration decisions yet.

            </div>

        `;

        return;
    }


    container.innerHTML =
        decisions.map(
            decision => {

                const cedarDecision =
                    formatDecision(
                        decision.cedar_decision ||
                        decision.decision ||
                        decision.status
                    );


                const decisionClass =
                    getDecisionClass(
                        cedarDecision
                    );


                const employee =
                    decision.from_employee ||
                    "—";


                const shift =
                    decision.shift_id ||
                    "—";


                const requestId =
                    decision.request_id ||
                    decision.pk ||
                    "—";


                const status =
                    decision.status ||
                    (
                        cedarDecision === "ALLOW"
                            ? "approved"
                            : "denied"
                    );


                const explanation =
                    decision.explanation ||
                    decision.reason ||
                    "No explanation available.";


                return `

                    <article
                        class="decision-card ${decisionClass}"
                    >


                        <div
                            class="decision-status-column"
                        >

                            <span
                                class="decision-status-dot ${
                                    decisionClass === "denied"
                                        ? "denied"
                                        : ""
                                }"
                            ></span>


                            <span
                                class="decision-status-text ${
                                    decisionClass === "denied"
                                        ? "denied"
                                        : ""
                                }"
                            >

                                ${escapeHTML(
                                    cedarDecision
                                )}

                            </span>

                        </div>


                        <div class="decision-main">

                            <div class="decision-route">

                                <span
                                    class="decision-employee"
                                >

                                    ${escapeHTML(
                                        employee
                                    )}

                                </span>


                                <span
                                    class="decision-arrow"
                                >

                                    →

                                </span>


                                <span
                                    class="decision-shift"
                                >

                                    ${escapeHTML(
                                        shift
                                    )}

                                </span>

                            </div>


                            <div
                                class="decision-explanation"
                            >

                                ${escapeHTML(
                                    explanation
                                )}

                            </div>

                        </div>


                        <div class="decision-meta">

                            <div class="decision-id">

                                #${escapeHTML(
                                    requestId
                                )}

                            </div>


                            <div
                                class="decision-status-badge ${
                                    decisionClass === "denied"
                                        ? "denied"
                                        : ""
                                }"
                            >

                                ${escapeHTML(
                                    status
                                )}

                            </div>

                        </div>


                    </article>

                `;
            }
        ).join("");
}


/* =========================================================
   SUBMIT SWAP REQUEST
   ========================================================= */

async function submitSwapRequest() {

    const employeeSelect =
        document.getElementById(
            "employeeSelect"
        );


    const shiftSelect =
        document.getElementById(
            "shiftSelect"
        );


    const reasonInput =
        document.getElementById(
            "reason"
        );


    const button =
        document.getElementById(
            "submitSwap"
        );


    const fromEmployee =
        employeeSelect
            ? employeeSelect.value
            : "";


    const shiftId =
        shiftSelect
            ? shiftSelect.value
            : "";


    const reason =
        reasonInput
            ? reasonInput.value.trim()
            : "";


    /* -----------------------------------------------------
       VALIDATION
       ----------------------------------------------------- */

    if (!fromEmployee) {

        alert(
            "Please select an employee."
        );

        return;
    }


    if (!shiftId) {

        alert(
            "Please select a shift."
        );

        return;
    }


    if (!reason) {

        alert(
            "Please enter a reason for the swap."
        );

        return;
    }


    /* -----------------------------------------------------
       LOADING STATE
       ----------------------------------------------------- */

    if (button) {

        button.disabled =
            true;

        button.dataset.originalText =
            button.innerHTML;

        button.innerHTML = `

            <span>
                PROCESSING...
            </span>

            <b>
                …
            </b>

        `;
    }


    try {


        /*
         * IMPORTANT:
         *
         * This payload is exactly what the
         * current backend expects.
         *
         * DO NOT change these field names.
         */

        const requestData = {

            from_employee:
                fromEmployee,

            shift_id:
                shiftId,

            reason:
                reason

        };


        console.log(
            "Submitting swap request:",
            requestData
        );


        const response =
            await fetch(
                `${API_URL}/swap-request`,
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            requestData
                        )

                }
            );


        let result = {};


        try {

            result =
                await response.json();

        } catch (jsonError) {

            console.warn(
                "Response was not valid JSON:",
                jsonError
            );


            result = {

                status:
                    "error",

                reason:
                    "The server returned an invalid response."

            };
        }


        console.log(
            "Swap request response:",
            response.status,
            result
        );


        /*
         * IMPORTANT:
         *
         * HTTP 403 from Cedar is an expected
         * business outcome, not a frontend crash.
         *
         * Show it as a DENY result card.
         */

        if (!response.ok) {

            const deniedResult = {

                ...result,

                cedar_decision:
                    result.cedar_decision ||
                    "DENY",

                status:
                    result.status ||
                    "denied",

                reason:
                    result.reason ||
                    result.cedar_reason ||
                    `Request rejected by API (HTTP ${response.status}).`

            };


            displayResult(
                deniedResult
            );

        } else {

            displayResult(
                result
            );
        }


        /*
         * Clear reason after successful
         * request only.
         */

        if (
            response.ok &&
            reasonInput
        ) {

            reasonInput.value =
                "";
        }


        /*
         * Refresh decision history.
         */

        await loadDecisions();


        /*
         * Refresh roster.
         */

        await loadRoster();


    } catch (error) {

        console.error(
            "Swap request failed:",
            error
        );


        const section =
            document.getElementById(
                "resultSection"
            );


        const card =
            document.getElementById(
                "resultCard"
            );


        if (
            section &&
            card
        ) {

            section.classList.remove(
                "hidden"
            );


            card.className =
                "result-card denied";


            card.innerHTML = `

                <div class="result-top">

                    <div>

                        <div class="section-eyebrow">

                            CONNECTION ERROR

                        </div>


                        <h3 style="
                            margin-top: 8px;
                            font-size: 24px;
                        ">

                            Unable to process request

                        </h3>

                    </div>


                    <div class="result-status">

                        ✕ ERROR

                    </div>

                </div>


                <div class="result-explanation">

                    ${escapeHTML(
                        error.message ||
                        "Unable to connect to the ShiftFair API."
                    )}


                    <br><br>


                    Make sure LocalStack,
                    DynamoDB and the SAM API
                    are running.

                </div>

            `;


            section.scrollIntoView({

                behavior:
                    "smooth",

                block:
                    "start"

            });
        }
    }


    finally {

        if (button) {

            button.disabled =
                false;


            button.innerHTML =
                button.dataset.originalText ||
                `
                    <span>
                        REQUEST FAIR SWAP
                    </span>

                    <b>
                        ↗
                    </b>
                `;

        }
    }
}


/* =========================================================
   THEME
   ========================================================= */

function initializeTheme() {

    const root =
        document.documentElement;


    const themeToggle =
        document.getElementById(
            "themeToggle"
        );


    const themeLabel =
        document.querySelector(
            ".theme-label"
        );


    const themeIcon =
        document.querySelector(
            ".theme-icon"
        );


    const metaTheme =
        document.querySelector(
            'meta[name="theme-color"]'
        );


    let savedTheme =
        null;


    try {

        savedTheme =
            localStorage.getItem(
                "shiftfair-theme"
            );

    } catch (error) {

        savedTheme =
            null;
    }


    const theme =
        savedTheme === "light"
            ? "light"
            : "dark";


    function applyTheme(
        selectedTheme
    ) {

        root.dataset.theme =
            selectedTheme;


        if (themeLabel) {

            themeLabel.textContent =
                selectedTheme.toUpperCase();
        }


        if (themeIcon) {

            themeIcon.textContent =
                selectedTheme === "dark"
                    ? "◐"
                    : "◑";
        }


        if (metaTheme) {

            metaTheme.setAttribute(
                "content",
                selectedTheme === "dark"
                    ? "#06100f"
                    : "#f3f7f5"
            );
        }
    }


    applyTheme(
        theme
    );


    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            () => {

                const nextTheme =
                    root.dataset.theme === "dark"
                        ? "light"
                        : "dark";


                applyTheme(
                    nextTheme
                );


                try {

                    localStorage.setItem(
                        "shiftfair-theme",
                        nextTheme
                    );

                } catch (error) {

                    console.warn(
                        "Could not save theme preference.",
                        error
                    );
                }

            }
        );
    }
}


/* =========================================================
   MOBILE NAVIGATION
   ========================================================= */

function initializeMobileNavigation() {

    const menu =
        document.getElementById(
            "mobileMenu"
        );


    const nav =
        document.querySelector(
            ".main-nav"
        );


    if (
        !menu ||
        !nav
    ) {
        return;
    }


    menu.addEventListener(
        "click",
        () => {

            const isOpen =
                nav.classList.toggle(
                    "open"
                );


            menu.setAttribute(
                "aria-expanded",
                String(
                    isOpen
                )
            );

        }
    );


    nav.querySelectorAll(
        "a"
    ).forEach(
        link => {

            link.addEventListener(
                "click",
                () => {

                    nav.classList.remove(
                        "open"
                    );


                    menu.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }
            );

        }
    );
}


/* =========================================================
   ACTIVE NAVIGATION
   ========================================================= */

function initializeActiveNavigation() {

    const sections = [
        "request",
        "roster",
        "history"
    ]
        .map(
            id =>
                document.getElementById(
                    id
                )
        )
        .filter(Boolean);


    const links =
        [
            ...document.querySelectorAll(
                ".main-nav a"
            )
        ];


    if (
        !(
            "IntersectionObserver"
            in window
        ) ||
        sections.length === 0
    ) {
        return;
    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(
                    entry => {

                        if (
                            !entry.isIntersecting
                        ) {
                            return;
                        }


                        links.forEach(
                            link => {

                                link.classList.toggle(
                                    "active",
                                    link.getAttribute(
                                        "href"
                                    ) ===
                                    `#${entry.target.id}`
                                );

                            }
                        );

                    }
                );

            },
            {
                rootMargin:
                    "-35% 0px -55% 0px",

                threshold:
                    0
            }
        );


    sections.forEach(
        section => {

            observer.observe(
                section
            );

        }
    );
}


/* =========================================================
   TERMINAL ANIMATION
   ========================================================= */

function initializeTerminalAnimation() {

    const lines =
        document.querySelectorAll(
            ".terminal-line"
        );


    lines.forEach(
        (
            line,
            index
        ) => {

            line.style.opacity =
                "0";


            line.style.transform =
                "translateX(-8px)";


            line.style.transition =
                "opacity .5s ease, transform .5s ease";


            setTimeout(
                () => {

                    line.style.opacity =
                        "1";


                    line.style.transform =
                        "none";

                },
                500 +
                index * 180
            );

        }
    );
}


/* =========================================================
   KINETIC NUMBER HELPER
   ========================================================= */

function initializeKineticNumberHelper() {

    window.animateKineticNumber =
        function (
            element,
            target
        ) {

            if (
                !element ||
                !Number.isFinite(
                    Number(target)
                )
            ) {
                return;
            }


            const finalValue =
                Number(target);


            const start =
                performance.now();


            const duration =
                1100;


            function tick(
                now
            ) {

                const progress =
                    Math.min(
                        (
                            now -
                            start
                        ) /
                        duration,
                        1
                    );


                const eased =
                    1 -
                    Math.pow(
                        1 -
                        progress,
                        4
                    );


                element.textContent =
                    Math.floor(
                        finalValue *
                        eased
                    );


                if (
                    progress < 1
                ) {

                    requestAnimationFrame(
                        tick
                    );

                } else {

                    element.textContent =
                        finalValue;
                }
            }


            requestAnimationFrame(
                tick
            );
        };
}


/* =========================================================
   EVENT LISTENERS
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "ShiftFair frontend initialized."
        );


        /*
         * Theme.
         */

        initializeTheme();


        /*
         * Mobile navigation.
         */

        initializeMobileNavigation();


        /*
         * Active navigation.
         */

        initializeActiveNavigation();


        /*
         * Scroll reveal.
         */

        initScrollReveal();


        /*
         * Terminal animation.
         */

        initializeTerminalAnimation();


        /*
         * Kinetic number helper.
         */

        initializeKineticNumberHelper();


        /*
         * Employee → shift.
         *
         * THIS IS THE KEY CONNECTION.
         *
         * Selecting an employee reloads
         * the shifts belonging to that employee.
         */

        const employeeSelect =
            document.getElementById(
                "employeeSelect"
            );


        if (employeeSelect) {

            employeeSelect.addEventListener(
                "change",
                () => {

                    console.log(
                        "Employee changed:",
                        employeeSelect.value
                    );


                    populateShiftDropdown();

                }
            );
        }


        /*
         * Submit button.
         */

        const submitButton =
            document.getElementById(
                "submitSwap"
            );


        if (submitButton) {

            submitButton.addEventListener(
                "click",
                submitSwapRequest
            );
        }


        /*
         * Load all backend data.
         */

        initializeDashboard();

    }
);


/* =========================================================
   INITIAL DASHBOARD LOAD
   ========================================================= */

async function initializeDashboard() {

    /*
     * Load roster first.
     */

    await loadRoster();


    /*
     * Then load decision history.
     */

    await loadDecisions();

}