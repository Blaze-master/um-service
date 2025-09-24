from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.message_service import get_intervention_content

router = APIRouter(prefix="/message", tags=["Message Optimizer"])

class MessageOptimizeRequest(BaseModel):
  intervention_id: str
  user_context: Optional[Dict[str, Any]] = None

@router.post("/optimize")
def optimize_message(request: MessageOptimizeRequest):
  """
  Given an intervention_id, return the optimized message content.
  Accepts optional user_context (e.g., {"name": "Kojo", "goal": "fitness"}).
  """
  result = get_intervention_content(
    intervention_id=request.intervention_id,
    user_context=request.user_context or {}
  )

  if result:
    return {"success": True, "intervention_data": result}
  return {"success": False, "error": "No matching message content found"}