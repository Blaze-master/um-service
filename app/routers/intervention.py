from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.intervention_service import resolve_intervention, llm_intervention
from app.services.message_service import get_intervention_content, get_intervention_content_old

router = APIRouter(prefix="/intervention", tags=["Intervention"])


class InterventionSelectRequest(BaseModel):
  user_state: str
  service_category: str
  user_context: Optional[Dict[str, Any]] = None

class UsageDataRequest(BaseModel):
  current: List[Dict[str, Any]]
  pastMilestones: List[Dict[str, Any]]
  pastInterventions: List[Dict[str, Any]]


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

    result = get_intervention_content_old(
      intervention_id=intervention_id,
      user_context=req.user_context or {}
    )
    
    results.append(result)

  return {"success": True, "result": results}

@router.post("/llm-select")
def llm_select_intervention(usage_data: UsageDataRequest):
  """
  Given usage data, select the most appropriate intervention using LLM.
  """
  interventionId = llm_intervention(usage_data.model_dump())
  result = get_intervention_content(
    intervention_id=interventionId,
    user_context={}
  ) if interventionId else None

  return {"success": True, "result": result, "intervention_id" : interventionId}