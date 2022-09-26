from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.routers import dependencies
from app.services.login import AuthService
from app.services.user import UserService

router = APIRouter(tags=["login"])


@router.post("/login", response_model=schemas.Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(dependencies.get_db),
):
    user = UserService.authenticate(db, username=form_data.username, password=form_data.password)
    tokens = await AuthService.get_access_refresh_tokens(user.id)
    return {**tokens, "token_type": "bearer"}


@router.post("/refresh", response_model=schemas.Token)
async def refresh_tokens(
        refresh_token: str = Body(...),
):
    tokens = await AuthService.refresh_tokens(refresh_token)
    return {**tokens, "token_type": "bearer"}
