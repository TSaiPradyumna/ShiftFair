const API_URL = "http://127.0.0.1:3000";


let rosterData = [];


/* =========================================
   LOAD APPLICATION
========================================= */

document.addEventListener(
    "DOMContentLoaded",

    async () => {

        await loadRoster();

        await loadDecisions();

    }
);


/* =========================================
   LOAD ROSTER
========================================= */

async function loadRoster() {

    try {

        console.log("Loading roster...");


        const response = await fetch(
            `${API_URL}/roster`
        );


        if (!response.ok) {

            throw new Error(
                `Roster request failed: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Roster data:",
            data
        );


        rosterData =
            data.roster || [];


        document.getElementById(
            "employeeCount"
        ).textContent =
            data.employee_count || 0;


        document.getElementById(
            "shiftCount"
        ).textContent =
            data.shift_count || 0;


        populateEmployeeDropdown();

        populateShiftDropdown();

        displayRoster();


        console.log(
            "Roster loaded successfully"
        );

    }

    catch (error) {

        console.error(
            "Roster error:",
            error
        );


        document.getElementById(
            "employeeCount"
        ).textContent = "Error";


        document.getElementById(
            "shiftCount"
        ).textContent = "Error";

    }

}


/* =========================================
   LOAD DECISIONS
========================================= */

async function loadDecisions() {

    try {

        console.log(
            "Loading decisions..."
        );


        const response = await fetch(
            `${API_URL}/decisions`
        );


        if (!response.ok) {

            throw new Error(
                `Decisions request failed: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Decision data:",
            data
        );


        document.getElementById(
            "decisionCount"
        ).textContent =
            data.decision_count || 0;


        displayDecisions(
            data.decisions || []
        );


        console.log(
            "Decisions loaded successfully"
        );

    }

    catch (error) {

        console.error(
            "Decision error:",
            error
        );


        document.getElementById(
            "decisionCount"
        ).textContent = "Error";

    }

}


/* =========================================
   EMPLOYEE DROPDOWN
========================================= */

function populateEmployeeDropdown() {

    const select =
        document.getElementById(
            "employeeSelect"
        );


    select.innerHTML = "";


    if (
        rosterData.length === 0
    ) {

        select.innerHTML =
            "<option>No employees available</option>";

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
       When employee changes,
       update the available shifts
    */

    select.addEventListener(

        "change",

        () => {

            populateShiftDropdown();

        }

    );

}


/* =========================================
   SHIFT DROPDOWN
========================================= */

function populateShiftDropdown() {

    const select =
        document.getElementById(
            "shiftSelect"
        );


    const employeeSelect =
        document.getElementById(
            "employeeSelect"
        );


    const selectedEmployeeId =
        employeeSelect.value;


    select.innerHTML = "";


    /*
       Find selected employee
    */

    const selectedEmployee =
        rosterData.find(

            employee =>

                employee.employee_id ===
                selectedEmployeeId

        );


    if (
        !selectedEmployee
    ) {

        select.innerHTML =
            "<option>No shifts available</option>";

        return;

    }


    const shifts =
        selectedEmployee.shifts || [];


    if (
        shifts.length === 0
    ) {

        select.innerHTML =
            "<option>No shifts available</option>";

        return;

    }


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

}


/* =========================================
   DISPLAY ROSTER
========================================= */

function displayRoster() {

    const roster =
        document.getElementById(
            "roster"
        );


    roster.innerHTML = "";


    if (
        rosterData.length === 0
    ) {

        roster.innerHTML =
            "<p>No employees found.</p>";

        return;

    }


    rosterData.forEach(

        employee => {

            let shiftsHTML = "";


            if (
                employee.shifts &&
                employee.shifts.length > 0
            ) {

                employee.shifts.forEach(

                    shift => {

                        shiftsHTML += `

                            <div class="shift">

                                <strong>
                                    ${shift.shift_id}
                                </strong>

                                <br>

                                ${shift.date}

                                <br>

                                ${shift.start_time}
                                -
                                ${shift.end_time}

                            </div>

                        `;

                    }

                );

            }

            else {

                shiftsHTML =
                    "<p>No shifts assigned.</p>";

            }


            roster.innerHTML += `

                <div class="employee-card">

                    <h3>
                        ${employee.name}
                    </h3>


                    <p>

                        <strong>ID:</strong>

                        ${employee.employee_id}

                    </p>


                    <p>

                        <strong>Role:</strong>

                        ${employee.role}

                    </p>


                    <p>

                        <strong>Department:</strong>

                        ${employee.department}

                    </p>


                    <div class="employee-shifts">

                        ${shiftsHTML}

                    </div>


                </div>

            `;

        }

    );

}


/* =========================================
   DISPLAY DECISIONS
========================================= */

function displayDecisions(
    decisions
) {

    const container =
        document.getElementById(
            "decisions"
        );


    container.innerHTML = "";


    if (
        decisions.length === 0
    ) {

        container.innerHTML = `

            <p>
                No decisions yet.
            </p>

        `;

        return;

    }


    decisions.forEach(

        decision => {

            container.innerHTML += `

                <div class="decision">

                    <h3>

                        Request

                        ${decision.request_id}

                    </h3>


                    <p>

                        <strong>
                            Employee:
                        </strong>

                        ${decision.from_employee}

                    </p>


                    <p>

                        <strong>
                            Shift:
                        </strong>

                        ${decision.shift_id}

                    </p>


                    <p>

                        <strong>
                            Suggested Partner:
                        </strong>

                        ${decision.suggested_partner_name || "No partner"}

                        ${
                            decision.suggested_partner
                            ?
                            `(${decision.suggested_partner})`
                            :
                            ""
                        }

                    </p>


                    <p>

                        <strong>
                            Eligible Partners:
                        </strong>

                        ${decision.eligible_partner_count || 0}

                    </p>


                    <p>

                        <strong>
                            Reason:
                        </strong>

                        ${decision.reason_text || "Not provided"}

                    </p>


                    <p>

                        <strong>
                            Explanation:
                        </strong>

                        ${decision.explanation || "No explanation available."}

                    </p>


                    <p>

                        <strong>
                            Status:
                        </strong>

                        ${decision.status || "Unknown"}

                    </p>


                </div>

            `;

        }

    );

}


/* =========================================
   SUBMIT SWAP REQUEST
========================================= */

document.getElementById(
    "submitSwap"
).addEventListener(

    "click",

    async () => {


        /*
           Get employee
        */

        const fromEmployee =
            document.getElementById(
                "employeeSelect"
            ).value;


        /*
           Get shift
        */

        const shiftId =
            document.getElementById(
                "shiftSelect"
            ).value;


        /*
           Get reason
        */

        const reason =
            document.getElementById(
                "reason"
            ).value.trim();


        /*
           Validation
        */

        if (
            !fromEmployee
        ) {

            alert(
                "Please select an employee."
            );

            return;

        }


        if (
            !shiftId
        ) {

            alert(
                "Please select a shift."
            );

            return;

        }


        if (
            !reason
        ) {

            alert(
                "Please enter a reason for the swap."
            );

            return;

        }


        const button =
            document.getElementById(
                "submitSwap"
            );


        button.textContent =
            "Processing...";


        button.disabled =
            true;


        try {


            /*
               IMPORTANT

               Backend expects:

               from_employee

               NOT:

               employee_id
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
                "Sending swap request:",
                requestData
            );


            const response =
                await fetch(

                    `${API_URL}/swap-request`,

                    {

                        method:
                            "POST",

                        headers:
                            {

                                "Content-Type":
                                    "application/json"

                            },


                        body:

                            JSON.stringify(
                                requestData
                            )

                    }

                );


            const result =
                await response.json();


            console.log(
                "Swap response:",
                result
            );


            /*
               Handle backend errors
            */

            if (
                !response.ok
            ) {

                throw new Error(

                    result.error ||

                    result.message ||

                    "Swap request failed."

                );

            }


            /*
               Display arbitration result
            */

            displayResult(
                result
            );


            /*
               Clear reason field
            */

            document.getElementById(
                "reason"
            ).value = "";


            /*
               Refresh decisions
            */

            await loadDecisions();


            /*
               Refresh roster
            */

            await loadRoster();


        }

        catch (error) {

            console.error(
                "Swap error:",
                error
            );


            alert(
                error.message ||
                "Something went wrong while processing the swap request."
            );

        }


        finally {

            button.textContent =
                "🔄 Request Fair Swap";


            button.disabled =
                false;

        }


    }

);


/* =========================================
   DISPLAY RESULT
========================================= */

function displayResult(
    result
) {

    const card =
        document.getElementById(
            "resultCard"
        );


    card.classList.remove(
        "hidden"
    );


    card.innerHTML = `

        <h3>

            🤖 ShiftFair Decision

        </h3>


        <p>

            <strong>
                Request ID:
            </strong>

            ${result.request_id || "N/A"}

        </p>


        <p>

            <strong>
                Status:
            </strong>

            ${result.status || "Processed"}

        </p>


        <p>

            <strong>
                Suggested Partner:
            </strong>

            ${result.suggested_partner_name || "No partner found"}

            ${
                result.suggested_partner
                ?
                `(${result.suggested_partner})`
                :
                ""
            }

        </p>


        <p>

            <strong>
                Eligible Partners:
            </strong>

            ${result.eligible_partner_count || 0}

        </p>


        <p>

            <strong>
                Explanation:
            </strong>

            ${result.explanation || "Decision processed successfully."}

        </p>

    `;


    document.getElementById(
        "resultSection"
    ).scrollIntoView(

        {

            behavior:
                "smooth"

        }

    );

}