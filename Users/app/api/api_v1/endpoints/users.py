from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import dependencies
from app.services.user import UserService

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
        *,
        db: Session = Depends(dependencies.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(dependencies.get_current_active_superuser),
):
    return UserService.get_user_list(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User)
async def create_user(
        *,
        db: Session = Depends(dependencies.get_db),
        user_in: schemas.UserCreate,
):
    return await UserService.create_user(db, obj_in=user_in)


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(dependencies.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.User = Depends(dependencies.get_current_active_user),
):
    # TODO pydantic
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email

    return UserService.update_user(db, db_obj=current_user, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def read_user_me(
        current_user: models.User = Depends(dependencies.get_current_active_user),
):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        *,
        db: Session = Depends(dependencies.get_db),
        user_id: int,
        current_user: models.User = Depends(dependencies.get_current_active_superuser),
):
    return UserService.get_user(db, id=user_id)


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(dependencies.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(dependencies.get_current_active_superuser),
):
    user = UserService.get_user(db, id=user_id)
    return UserService.update_user(db, db_obj=user, obj_in=user_in)
