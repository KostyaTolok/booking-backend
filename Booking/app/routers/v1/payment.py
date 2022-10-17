from fastapi import Header, Request, Depends, APIRouter
from aiohttp import ClientSession
from sqlalchemy.orm import Session

from app.core.config import config
from app.crud.payment import BookingCRUD
from app.routers.dependences import get_active_token_payload, get_db, get_http_client
from app import schemas
from app.services.booking import BookingServices
from app.services.apartment import ApartmentServices
from app.services.stripe import StripeService

router = APIRouter(tags=["payment"])


@router.post("/payment-sheet", response_model=schemas.PaymentSheet)
async def payment_sheet(
    db: Session = Depends(get_db),
    client: ClientSession = Depends(get_http_client),
    *,
    payload: schemas.Booking,
    token_payload: schemas.Token = Depends(get_active_token_payload),
):
    apartment = await ApartmentServices.fetch_apartment(
        client,
        apartment_id=payload.apartment_id,
    )
    total_price = BookingServices.calculate_price(
        start_date=payload.start_date,
        end_date=payload.end_date,
        price_per_night=apartment.price,
    )
    BookingServices.check_booking_dates_availability(
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

    booking = schemas.BookingCreate(
        payment_intent_id=payment_intent.id,
        customer_id=customer.id,
        user_id=token_payload.sub,
        apartment_id=payload.apartment_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        price=total_price,
    )
    BookingCRUD.create(db, booking)

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
    event = await StripeService.construct_event(data, stripe_signature)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        BookingServices.confirm_payment(db, payment_intent["id"])

    return {"status": "success"}
