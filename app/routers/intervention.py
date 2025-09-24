from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.intervention_service import get_intervention_for_milestone

router = APIRouter()

class InterventionRequest(BaseModel):
    milestone_id: str
    app_name: str | None = None

class InterventionResponse(BaseModel):
    intervention_id: str

@router.post("/select", response_model=InterventionResponse)
def select_intervention(req: InterventionRequest):
    try:
        intervention_id = get_intervention_for_milestone(req.milestone_id, req.app_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not intervention_id:
        raise HTTPException(status_code=404, detail="No intervention found for milestone")

    return {"intervention_id": intervention_id}
