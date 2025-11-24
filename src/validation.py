"""
Validation utilities for JSON extraction outputs.

This module stores:
- the JSON field schema
- controlled vocabularies
- a simple validation helper
"""

from typing import Dict, Any, List, Optional


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
# CONTROLLED VOCULARIES
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
def validate_extracted_json(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate that the extracted JSON object matches the expected schema.

    Checks:
    - All required fields exist
    - Correct types (string or list)
    - Controlled vocabulary fields are valid

    Returns
    -------
    dict or None
        The cleaned dictionary if valid, or None if invalid.
    """

    # Check presence of all fields
    for field, expected_type in FIELD_SCHEMA.items():
        if field not in data:
            print(f"Missing field: {field}")
            return None

    # Type checks
    for field, expected_type in FIELD_SCHEMA.items():
        value = data[field]

        if expected_type == "string":
            if not isinstance(value, str):
                print(f"Field {field} must be a string")
                return None

        if expected_type == "list":
            if not isinstance(value, list):
                print(f"Field {field} must be a list")
                return None

    # Controlled vocabulary checks
    # Empty string is allowed here, since the model may leave it blank
    risk_type = data.get("risk_type", "")
    if risk_type and risk_type not in ALLOWED_RISK_TYPES:
        print(f"Invalid risk_type: {risk_type}")
        return None

    region = data.get("region", "")
    if region and region not in ALLOWED_REGIONS:
        print(f"Invalid region: {region}")
        return None

    time_horizon = data.get("time_horizon", "")
    if time_horizon and time_horizon not in ALLOWED_TIME_HORIZONS:
        print(f"Invalid time_horizon: {time_horizon}")
        return None

    # If everything passes, return the cleaned dictionary
    return data
