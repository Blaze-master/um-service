import json
from pathlib import Path
from typing import Optional, Dict, Any


# Load intervention library once at startup
LIBRARY_PATH = Path(__file__).resolve().parent.parent / "data" / "intervention_library.json"
with open(LIBRARY_PATH, "r") as f:
  INTERVENTION_LIBRARY = json.load(f)


def resolve_intervention(user_state: str, service_category: str) -> Optional[Dict[str, Any]]:
  """
  Resolves an intervention based on user_state and service_category.
  - If service_category = UNITI → fixed.
  - If service_category placeholder → substitute with actual value.
  - Templates also support {name}, {goal}, {service_category}.
  """

  for entry in INTERVENTION_LIBRARY:
    trigger = entry["trigger"]

    if (trigger["user_state"] == user_state) and (trigger["service_category"] == service_category):
      return entry["data"]["intervention_id"]

  return None
