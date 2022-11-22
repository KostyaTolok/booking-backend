from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.routers import dependencies
from app.services.confirm import ConfirmService
from app.services.user import UserService

router = APIRouter(tags=["confirm"])


@router.post("/reset-password", response_model=schemas.Message)
async def reset_password(
    *,
    db: Session = Depends(dependencies.get_db),
    email: str = Body(..., embed=True),
):
    user = UserService.get_user_by_email(db, email=email)
    await ConfirmService.send_recover_password_email(db, user=user)
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/confirm", response_model=schemas.Message)
def confirm_password_reset(
    *,
    db: Session = Depends(dependencies.get_db),
    body: schemas.Reset,
):
    ConfirmService.reset_password(db, token=body.token, new_password=body.new_password)
    return {"msg": "Password updated successfully"}


@router.post("/verify-email", response_model=schemas.Message)
async def send_email_confirmation_code(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    await ConfirmService.send_email_confirmation_code(current_user)
    return {"msg": "Code sent to email"}


@router.post("/verify-email/confirm", response_model=schemas.Message)
async def confirm_email(
    *,
    db: Session = Depends(dependencies.get_db),
    code: str = Body(..., embed=True),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    await ConfirmService.confirm_email(db, user=current_user, code=code)
    return {"msg": "Email confirmed successfully"}
