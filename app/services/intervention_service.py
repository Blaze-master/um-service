import json
from ..config import get_settings
from .llm_service import prompt_llm
from ..utils.prompts import INTERVENTION_PROMPT, INTERVENTION_TYPES
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

def llm_intervention(usage_data: Any) -> str:
  settings = get_settings()
  params = {"usage_data" : usage_data, "milestone_to_intervention_types" : settings.milestones_to_intervention, "intervention_types" : INTERVENTION_TYPES}
  intervention = prompt_llm(INTERVENTION_PROMPT,params)
  return intervention