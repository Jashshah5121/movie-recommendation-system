from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.movies import router as movie_router
from app.routers.search import router as search_router
from app.routers.recommendations import router as recommendation_router
from app.routers.movie_details import router as movie_details_router
from app.routers.discover import router as discover_router
from app.routers import ai_recommend
from app.routers.similar_movies import router as similar_movies_router
from app.routers.ai import router as ai_router
from app.routers.smart_search import router as smart_search_router
app = FastAPI(
    title="Movie Recommendation API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
         "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(movie_router)
app.include_router(search_router)
app.include_router(recommendation_router)
app.include_router(movie_details_router)
app.include_router(discover_router)
app.include_router(ai_recommend.router)
app.include_router(similar_movies_router)
app.include_router(ai_router)
app.include_router(smart_search_router)

@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API is running successfully!"
    }