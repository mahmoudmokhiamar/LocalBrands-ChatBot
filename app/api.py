from fastapi import APIRouter
from .models import RecommendRequest, RecommendResponse
from .pipeline import get_recommendation

router = APIRouter()

@router.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    result = get_recommendation(request.query)
    return RecommendResponse(result=result)