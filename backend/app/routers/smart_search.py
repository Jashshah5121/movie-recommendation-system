from fastapi import APIRouter
from pydantic import BaseModel

from app.services.smart_search_service import SmartSearchService

router = APIRouter(prefix="/search", tags=["Smart Search"])


class SearchRequest(BaseModel):
    query: str


@router.post("/smart")
def smart_search(request: SearchRequest):
    return SmartSearchService.search(request.query)