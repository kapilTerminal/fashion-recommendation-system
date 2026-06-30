from fastapi import FastAPI

from .api.health import router as health_router
from .api.recommendation import router as recommendation_router

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Fashion Recommendation System"
    }


app.include_router(health_router)
app.include_router(recommendation_router)