from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["MovieHub AI"]
)


class AIRequest(BaseModel):

    query:str


@router.post("/search")

def search(request:AIRequest):

    return AIService.search(request.query)