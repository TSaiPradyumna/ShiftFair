"""
Run standalone first: python3 swap_agent.py
This tests the agent's reasoning in isolation before wiring it into the Lambda.

NOTE: exact Strands import syntax may vary by SDK version - check their
quickstart repo if this import fails, and tell Claude the error so it can
be corrected.
"""
from strands import Agent

# A tool the agent can call - reads eligible colleagues (mocked for now,
# replace with a real DynamoDB/OpenSearch lookup once wired in)
def get_eligible_colleagues(shift_id: str) -> list:
    """Returns colleagues who passed the Cedar fairness check for this shift."""
    return [
        {"employee_id": "E002", "recent_night_shifts": 1, "role": "guard"},
        {"employee_id": "E004", "recent_night_shifts": 0, "role": "guard"},
    ]

agent = Agent(
    tools=[get_eligible_colleagues],
    system_prompt=(
        "You are a fairness-focused shift-swap assistant. Given a swap request "
        "and a list of Cedar-eligible colleagues, recommend the fairest partner "
        "(prefer the one with fewer recent night shifts) and explain your choice "
        "in exactly 2 plain-English sentences. Do not mention Cedar or JSON."
    ),
)

if __name__ == "__main__":
    prompt = (
        "Employee E001 wants to swap shift S045 (a night shift) because of a "
        "family event. Who should take it and why?"
    )
    result = agent(prompt)
    print("\n--- Agent response ---")
    print(result)
