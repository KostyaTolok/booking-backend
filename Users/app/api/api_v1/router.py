from fastapi import APIRouter

from app.api.api_v1.endpoints import auth
from app.api.api_v1.endpoints import users
from app.api.api_v1.endpoints import confirm


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth",  tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(confirm.router, prefix="/users",  tags=["confirm"])

