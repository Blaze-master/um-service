from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.intervention_service import resolve_intervention

router = APIRouter(prefix="/intervention", tags=["Intervention"])


class InterventionSelectRequest(BaseModel):
  user_state: str
  service_category: str


@router.post("/select")
def select_intervention(request: InterventionSelectRequest):
  """
  Given a user_state and service_category, return the matching intervention.
  """
  result = resolve_intervention(
    user_state=request.user_state,
    service_category=request.service_category,
  )

  if result:
    return {"success": True, "intervention": result}
  return {"success": False, "error": "No matching intervention found"}
