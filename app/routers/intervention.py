from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.intervention_service import resolve_intervention

router = APIRouter(prefix="/interventions", tags=["Interventions"])


class InterventionSelectRequest(BaseModel):
    milestone: str
    service_category: str
    user_context: Optional[Dict[str, Any]] = None


@router.post("/select")
def get_intervention(request: InterventionSelectRequest):
    """
    Given a milestone and service_category, return the matching intervention.
    Accepts optional user_context (e.g., {"name": "Kojo", "goal": "fitness"}).
    """
    result = resolve_intervention(
        milestone=request.milestone,
        service_category=request.service_category,
        user_context=request.user_context or {}
    )

    if result:
        return {"success": True, "intervention": result}
    return {"success": False, "error": "No matching intervention found"}
