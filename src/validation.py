"""
Validation utilities for JSON extraction outputs.

This module stores:
- the JSON field schema
- controlled vocabularies
- a simple validation helper
"""

from typing import Dict, Any, List


# ---------------------------------------------
# JSON FIELD SCHEMA
# ---------------------------------------------
FIELD_SCHEMA: Dict[str, str] = {
    "entity_name": "string",
    "region": "string",
    "sector": "string",
    "risk_type": "string",
    "time_horizon": "string",
    "key_risk_factors": "list",
    "risk_summary": "string",
}


# ---------------------------------------------
# CONTROLLED VOCABULARIES
# ---------------------------------------------
ALLOWED_RISK_TYPES: List[str] = [
    "property",
    "marine",
    "motor",
    "cyber",
    "liability",
    "health",
    "travel",
    "esg",
    "operational",
    "other",
]

ALLOWED_REGIONS: List[str] = [
    "global",
    "europe",
    "north_america",
    "asia_pacific",
    "latin_america",
    "middle_east_africa",
]

ALLOWED_TIME_HORIZONS: List[str] = [
    "short_term",
    "medium_term",
    "long_term",
    "multi_horizon",
    "not_specified",
]


# ---------------------------------------------
# SIMPLE VALIDATION HELPER
# ---------------------------------------------
def validate_extracted_json(data: Dict[str, Any]) -> bool:
    """
    Simple validation check for LLM JSON output.

    Checks:
    - All required fields exist
    - Correct types (string or list)
    - Controlled vocabulary fields are valid

    Returns True if valid, False otherwise.
    """

    # Check presence of all fields
    for field in FIELD_SCHEMA.keys():
        if field not in data:
            print(f"Missing field: {field}")
            return False

    # Type checks
    for field, expected_type in FIELD_SCHEMA.items():
        if expected_type == "string" and not isinstance(data[field], str):
            print(f"Field {field} must be a string")
            return False
        if expected_type == "list" and not isinstance(data[field], list):
            print(f"Field {field} must be a list")
            return False

    # Controlled vocabulary checks
    if data["risk_type"] not in ALLOWED_RISK_TYPES:
        print(f"Invalid risk_type: {data['risk_type']}")
        return False

    if data["region"] not in ALLOWED_REGIONS:
        print(f"Invalid region: {data['region']}")
        return False

    if data["time_horizon"] not in ALLOWED_TIME_HORIZONS:
        print(f"Invalid time_horizon: {data['time_horizon']}")
        return False

    return True
