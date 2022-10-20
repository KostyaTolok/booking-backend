from fastapi import Header, Request, Depends, APIRouter
from aiohttp import ClientSession
from sqlalchemy.orm import Session

from app.core.config import config
from app.crud.payment import PaymentCRUD
from app.routers.dependences import get_active_token_payload, get_db, get_http_client
from app import schemas
from app.services.booking import PaymentServices
from app.services.apartment import ApartmentServices
from app.services.stripe import StripeService

router = APIRouter(tags=["payment"])


@router.post("/payment-sheet", response_model=schemas.PaymentSheet)
async def payment_sheet(
    db: Session = Depends(get_db),
    client: ClientSession = Depends(get_http_client),
    *,
    payload: schemas.Payment,
    token_payload: schemas.Token = Depends(get_active_token_payload),
):
    apartment = await ApartmentServices.fetch_apartment(
        client,
        apartment_id=payload.apartment_id,
    )
    total_price = PaymentServices.calculate_price(
        start_date=payload.start_date,
        end_date=payload.end_date,
        price_per_night=apartment.price,
    )
    PaymentServices.check_booking_dates_availability(
        db,
        apartment_id=payload.apartment_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )

    customer, ephemeral_key = await StripeService.create_customer(token_payload.sub)
    payment_intent = await StripeService.create_payment_intent(
        customer_id=customer.id,
        customer_email=token_payload.email,
        price=total_price,
    )

    booking = schemas.PaymentCreate(
        payment_intent_id=payment_intent.id,
        customer_id=customer.id,
        user_id=token_payload.sub,
        apartment_id=payload.apartment_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        price=total_price,
    )
    PaymentCRUD.create(db, booking)

    return {
        "payment_intent": payment_intent.id,
        "ephemeral_key": ephemeral_key.secret,
        "customer": customer["id"],
        "publishable_key": config.STRIPE_PUBLISHABLE_KEY,
    }


@router.post("/webhook")
async def webhook_received(
    db: Session = Depends(get_db),
    *,
    request: Request,
    stripe_signature: str = Header(),
):
    data = await request.body()
    event = StripeService.construct_event(data, stripe_signature)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        await PaymentServices.confirm_payment(db, "pi_3LuuFtA6LTxBASfH1Iz166H8")

    return {"status": "success"}
