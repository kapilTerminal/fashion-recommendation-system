from fastapi import APIRouter
from ..schemas.recommendation import UserPreference
from ..services.recommendation_service import recommendation_service

router = APIRouter()


@router.post("/recommend")
def recommend(data: UserPreference):
    return recommendation_service(data)