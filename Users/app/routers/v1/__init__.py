from fastapi import APIRouter

from app.routers.v1.auth import router as auth_router
from app.routers.v1.confirm import router as confirm_router
from app.routers.v1.users import router as users_router

router = APIRouter()

router.include_router(
    auth_router,
    prefix="/auth"
)

router.include_router(
    confirm_router,
    prefix="/users"
)

router.include_router(
    users_router,
    prefix="/users"
)
