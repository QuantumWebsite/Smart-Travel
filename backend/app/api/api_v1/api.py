from fastapi import APIRouter

from app.api.api_v1.endpoints import search, users, auth, recommendations, deals

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(deals.router, prefix="/deals", tags=["deals"])