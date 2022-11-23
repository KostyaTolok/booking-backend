from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.routers import dependencies
from app.services.auth import AuthService
from app.services.user import UserService

router = APIRouter(tags=["login"])


@router.post("/login", response_model=schemas.Tokens)
async def login(
    db: Session = Depends(dependencies.get_db),
    *,
    login_data: schemas.Login,
):
    user = UserService.authenticate(
        db, username=login_data.email, password=login_data.password
    )
    tokens = await AuthService.get_access_refresh_tokens(
        db, user_id=user.id, user_email=user.email, user_active=user.is_active
    )
    return {**tokens, "token_type": "bearer"}


@router.post("/login/form", response_model=schemas.Tokens)
async def login(
    db: Session = Depends(dependencies.get_db),
    *,
    login_data: OAuth2PasswordRequestForm = Depends(),
):
    user = UserService.authenticate(
        db, username=login_data.username, password=login_data.password
    )
    tokens = await AuthService.get_access_refresh_tokens(
        db, user_id=user.id, user_email=user.email, user_active=user.is_active
    )
    return {**tokens, "token_type": "bearer"}


@router.post("/refresh", response_model=schemas.Tokens)
async def refresh_tokens(
    db: Session = Depends(dependencies.get_db),
    refresh_token: str = Body(..., embed=True),
):
    tokens = await AuthService.refresh_tokens(db, refresh_token=refresh_token)
    return {**tokens, "token_type": "bearer"}
