"""
Reducer utilities to merge chunk-level LLM outputs into document-level JSON records.

This module assumes that:
- Each chunk has already been processed by the LLM.
- Each chunk-level result is a validated dict that follows the common schema:
  {
      "entity_name": str,
      "region": str,
      "sector": str,
      "risk_type": str,
      "time_horizon": str,
      "key_risk_factors": list[str],
      "risk_summary": str,
  }

The goal is to combine many chunk-level dicts into a single document-level dict.
"""

from typing import List, Dict, Any, Optional
from collections import Counter

from .validation import (
    ALLOWED_RISK_TYPES,
    ALLOWED_REGIONS,
    ALLOWED_TIME_HORIZONS,
)


def _clean_str(value: Any) -> str:
    """
    Safely convert a value to a stripped string.
    Returns an empty string if the value is not a string or is blank.
    """
    if not isinstance(value, str):
        return ""
    cleaned = value.strip()
    return cleaned if cleaned else ""


def _choose_most_frequent_non_empty(values: List[str]) -> str:
    """
    Helper to pick the most common non-empty string from a list.

    If all values are empty strings, returns an empty string.
    """
    cleaned = [_clean_str(v) for v in values]
    cleaned = [v for v in cleaned if v]

    if not cleaned:
        return ""

    counts = Counter(cleaned)
    most_common_value, _ = counts.most_common(1)[0]
    return most_common_value


def _merge_lists_unique(list_of_lists: List[List[str]]) -> List[str]:
    """
    Merge several lists of strings into a single list with unique values,
    while preserving the order of first appearance.

    Uniqueness is checked in a case-insensitive way, but the original
    casing of the first occurrence is preserved.
    """
    seen_lower = set()
    merged: List[str] = []

    for items in list_of_lists:
        if not isinstance(items, list):
            continue
        for item in items:
            cleaned = _clean_str(item)
            if not cleaned:
                continue
            key_lower = cleaned.lower()
            if key_lower in seen_lower:
                continue
            seen_lower.add(key_lower)
            merged.append(cleaned)

    return merged


def _concat_summaries(summaries: List[str], max_chars: int = 800) -> str:
    """
    Concatenate multiple summary strings into one document-level summary.

    The result is truncated to at most max_chars characters to avoid
    extremely long text.
    """
    cleaned = [_clean_str(s) for s in summaries]
    cleaned = [s for s in cleaned if s]

    if not cleaned:
        return ""

    combined = " ".join(cleaned)

    if len(combined) > max_chars:
        combined = combined[:max_chars].rstrip()
        # Optional: add an ellipsis to indicate truncation
        combined = combined + " ..."

    return combined


def reduce_extractions_for_document(
    chunk_extractions: List[Dict[str, Any]],
    doc_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Reduce a list of chunk-level extraction dicts into a single document-level dict.

    Parameters
    ----------
    chunk_extractions : List[Dict[str, Any]]
        A list of validated extraction results for a single document.
        Each dict must follow the common JSON schema.

    doc_metadata : Optional[Dict[str, Any]], optional
        Optional metadata about the document, for example:
        {
            "category": "policy",
            "filename": "auto_insurance_policy_synthetic.txt",
            "doc_index": 6,
        }
        These fields are not part of the core schema, but can be
        attached to the final result for convenience.

    Returns
    -------
    Dict[str, Any]
        A document-level JSON dict that follows the same schema:
        {
            "entity_name": ...,
            "region": ...,
            "sector": ...,
            "risk_type": ...,
            "time_horizon": ...,
            "key_risk_factors": [...],
            "risk_summary": ...
        }
        plus any extra metadata fields if provided.
    """
    # Filter out any non-dict or None values defensively
    valid_dicts = [c for c in chunk_extractions if isinstance(c, dict)]

    if not valid_dicts:
        # No valid chunk outputs, return empty schema with optional metadata
        doc_level: Dict[str, Any] = {
            "entity_name": "",
            "region": "",
            "sector": "",
            "risk_type": "",
            "time_horizon": "",
            "key_risk_factors": [],
            "risk_summary": "",
        }
        if doc_metadata:
            doc_level.update(doc_metadata)
        return doc_level

    # Collect values for each field across all chunks
    entity_names = [c.get("entity_name", "") for c in valid_dicts]
    sectors = [c.get("sector", "") for c in valid_dicts]
    risk_types = [c.get("risk_type", "") for c in valid_dicts]
    regions = [c.get("region", "") for c in valid_dicts]
    time_horizons = [c.get("time_horizon", "") for c in valid_dicts]
    risk_factor_lists = [c.get("key_risk_factors", []) for c in valid_dicts]
    summaries = [c.get("risk_summary", "") for c in valid_dicts]

    # Aggregate categorical fields using a simple majority vote
    entity_name = _choose_most_frequent_non_empty(entity_names)
    sector = _choose_most_frequent_non_empty(sectors)

    # For controlled vocab fields, choose the most frequent valid value.
    # Comparison is done in a case-insensitive way, but output uses
    # the canonical value from the allowed lists.
    allowed_risk_types_lower = {v.lower(): v for v in ALLOWED_RISK_TYPES}
    allowed_regions_lower = {v.lower(): v for v in ALLOWED_REGIONS}
    allowed_time_horizons_lower = {v.lower(): v for v in ALLOWED_TIME_HORIZONS}

    risk_type_candidate = _choose_most_frequent_non_empty(risk_types)
    risk_type_key = risk_type_candidate.lower()
    risk_type = (
        allowed_risk_types_lower.get(risk_type_key, "other")
    )

    region_candidate = _choose_most_frequent_non_empty(regions)
    region_key = region_candidate.lower()
    region = (
        allowed_regions_lower.get(region_key, "global")
    )

    time_horizon_candidate = _choose_most_frequent_non_empty(time_horizons)
    time_horizon_key = time_horizon_candidate.lower()
    time_horizon = (
        allowed_time_horizons_lower.get(time_horizon_key, "not_specified")
    )

    # Aggregate list and summary fields
    key_risk_factors = _merge_lists_unique(risk_factor_lists)
    risk_summary = _concat_summaries(summaries, max_chars=800)

    # Build the final document-level record
    doc_level: Dict[str, Any] = {
        "entity_name": entity_name,
        "region": region,
        "sector": sector,
        "risk_type": risk_type,
        "time_horizon": time_horizon,
        "key_risk_factors": key_risk_factors,
        "risk_summary": risk_summary,
    }

    # Optionally attach extra metadata, such as category or filename
    if doc_metadata:
        doc_level.update(doc_metadata)

    return doc_level
