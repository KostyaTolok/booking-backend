from fastapi import APIRouter

from app.routers.v1 import router as v1_router

router = APIRouter()

router.include_router(
    v1_router,
    prefix="/v1"
)
