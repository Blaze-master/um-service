from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.intervention_service import resolve_intervention
from app.services.message_service import get_intervention_content

router = APIRouter(prefix="/intervention", tags=["Intervention"])


class InterventionSelectRequest(BaseModel):
  user_state: str
  service_category: str
  user_context: Optional[Dict[str, Any]] = None


@router.post("/select")
def select_interventions(requests: List[InterventionSelectRequest]):
  """
  Given a list of user_state and service_category objects, 
  return the matching interventions.
  """
  results = []
  for req in requests:
    intervention_id = resolve_intervention(
      user_state=req.user_state,
      service_category=req.service_category,
    ) or "UNKNOWN"

    result = get_intervention_content(
      intervention_id=intervention_id,
      user_context=req.user_context or {}
    )
    
    results.append(result)

  return {"success": True, "result": results}
