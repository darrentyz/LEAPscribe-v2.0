import re

CAPABILITY_BEST_PRACTICES = [
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.1",
        "statement": "Finance collaborates with business/ops/policy departments to build detailed departmental budgets.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.2",
        "statement": "Finance uses historical data as the basis for budgeting for all departments.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.3",
        "statement": "Finance sets key budget assumptions centrally for operating and development expenditure.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.4",
        "statement": "Finance uses detailed spreadsheets to collect and consolidate budget proposals from each department.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.5",
        "statement": "Finance establishes clear roles and responsibilities for Finance and departmental budget owners in the budgeting process.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.6",
        "statement": "Finance pre-loads standard assumptions and forecasts to limit inputs for bottom-up budget submissions.",
    },
    {
        "cap_id": "1.1",
        "capability": "Perform Intelligent Budget Planning",
        "metric_id": "1.1.7",
        "statement": "Finance consolidates bottom-up budget submissions for analysis and challenge.",
    },
]

def get_all_best_practices():
    return CAPABILITY_BEST_PRACTICES

def parse_questions_list(text: str):
    items = re.findall(r"[-•]\s*(.+)", text)
    return [i.strip() for i in items[:10]]

def parse_bp_ids(text: str):
    return list(sorted(set(re.findall(r"\d+\.\d+\.\d+", text))))
