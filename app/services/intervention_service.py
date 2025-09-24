import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data"

def load_intervention_mappings():
    with open(DATA_PATH / "milestones_to_interventions.json") as f:
        return json.load(f)

def get_intervention_for_milestone(milestone_id: str, app_name: str = None):
    mappings = load_intervention_mappings()
    match = next((m for m in mappings if m["milestone_id"] == milestone_id), None)
    
    if not match:
        return None

    intervention_id = match["intervention_id"]
    
    # Replace placeholder if necessary
    if "{app_name}" in intervention_id:
        if not app_name:
            raise ValueError("app_name is required for this milestone")
        intervention_id = intervention_id.replace("{app_name}", app_name)

    return intervention_id
