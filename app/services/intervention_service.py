import json
from pathlib import Path
from typing import Optional, Dict, Any


# Load intervention library once at startup
LIBRARY_PATH = Path(__file__).resolve().parent.parent / "data" / "intervention_library.json"
with open(LIBRARY_PATH, "r") as f:
    INTERVENTION_LIBRARY = json.load(f)


def resolve_intervention(milestone: str, service_category: str, user_context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Resolves an intervention based on milestone and service_category.
    - If service_category = UNITI → fixed.
    - If service_category placeholder → substitute with actual value.
    - Templates also support {name}, {goal}, {service_category}.
    """

    for entry in INTERVENTION_LIBRARY:
        trigger = entry["trigger"]

        if trigger["milestone"] == milestone:
            lib_category = trigger["service_category"]

            # Match UNITI directly
            if lib_category == "UNITI" and service_category == "UNITI":
                return _fill_placeholders(entry["data"], user_context, service_category)

            # Handle category substitution
            if lib_category == "{service_category}" and service_category != "UNITI":
                return _fill_placeholders(entry["data"], user_context, service_category)

    return None


def _fill_placeholders(data: Dict[str, Any], user_context: Optional[Dict[str, Any]], service_category: str) -> Dict[str, Any]:
    """Fill dynamic placeholders in intervention_id and template."""
    filled = data.copy()

    # Replace {service_category} placeholder
    filled["intervention_id"] = filled["intervention_id"].replace("{service_category}", service_category)
    filled["template"] = filled["template"].replace("{service_category}", service_category)

    # Replace other placeholders from user_context
    if user_context:
        for key, value in user_context.items():
            if value is not None:
                filled["template"] = filled["template"].replace(f"{{{key}}}", str(value))

    return filled
