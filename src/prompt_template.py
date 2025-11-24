# src/prompt_template.py

from typing import List

from .validation import (
    ALLOWED_REGIONS,
    ALLOWED_RISK_TYPES,
    ALLOWED_TIME_HORIZONS,
)

PROMPT_TEMPLATE = """
You are an AI assistant that extracts structured risk information from insurance related text.

Your task:
- Read the provided document chunk carefully.
- Extract the requested fields based only on information in this chunk.
- If a field is not mentioned or cannot be inferred with high confidence, leave it as an empty string "" or an empty list [].

Output format:
Return a single JSON object with exactly these fields:
- entity_name (string)
- region (string, one of: {allowed_regions})
- sector (string)
- risk_type (string, one of: {allowed_risk_types})
- time_horizon (string, one of: {allowed_time_horizons})
- key_risk_factors (list of strings)
- risk_summary (string, 1 to 3 sentences)

Constraints:
- Use only the fields listed above. Do not add extra fields.
- Use only the allowed values for risk_type, region, and time_horizon.
- Do not invent entities, locations, or risks that are not supported by the text.
- If the text does not specify a value, use an empty string "" or an empty list [].
- Respond with valid JSON only. Do not include any explanations, comments, or markdown.

Document chunk:
{chunk_text}
""".strip()


def build_prompt(chunk_text: str) -> str:
    """
    Build a formatted LLM prompt by filling the JSON schema
    and inserting the document chunk.

    Parameters
    ----------
    chunk_text : str
        The text of a single chunk.

    Returns
    -------
    str
        The final prompt to send to the LLM.
    """
    return PROMPT_TEMPLATE.format(
        allowed_regions=", ".join(ALLOWED_REGIONS),
        allowed_risk_types=", ".join(ALLOWED_RISK_TYPES),
        allowed_time_horizons=", ".join(ALLOWED_TIME_HORIZONS),
        chunk_text=chunk_text.strip(),
    )
