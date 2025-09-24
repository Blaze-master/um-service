from fastapi import APIRouter
from app.services.message_service import *

router = APIRouter(prefix="/message", tags=["Message Optimizer"])