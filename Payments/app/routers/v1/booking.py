from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.routers.dependences import get_active_token_payload, get_db
from app import schemas
from app.services.payment import PaymentServices

router = APIRouter(tags=["booking"])


@router.get("/booked-apartment", response_model=List[schemas.PaymentRetrieve])
def get_booked_apartments(
    db: Session = Depends(get_db),
    token_payload: schemas.Token = Depends(get_active_token_payload),
):
    return PaymentServices.get_users_booked_apartments(db, token_payload.sub)
