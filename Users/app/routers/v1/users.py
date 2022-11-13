from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.routers import dependencies
from app.services.user import UserService

router = APIRouter(tags=["users"])


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
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(dependencies.get_current_user),
):
    return UserService.update_user(db, db_obj=current_user, obj_in=user_in)


@router.delete("/me", response_model=schemas.User)
def delete_user_me(
        *,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
):
    return UserService.delete_user(db, current_user.id)


@router.get("/me", response_model=schemas.User)
def read_user_me(
        current_user: models.User = Depends(dependencies.get_current_user),
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


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
        *,
        db: Session = Depends(dependencies.get_db),
        user_id: int,
        current_user: models.User = Depends(dependencies.get_current_active_superuser),
):
    return UserService.delete_user(db, user_id)
