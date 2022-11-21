import logging

from fastapi import Header, Request, Depends, APIRouter
from aiohttp import ClientSession
from sqlalchemy.orm import Session

from app.routers.dependences import get_active_token_payload, get_db, get_http_client
from app import schemas
from app.services.payment import PaymentServices
from app.services.apartment import ApartmentServices
from app.services.stripe import StripeService

router = APIRouter(tags=["payment"])


@router.post("/payment-sheet", response_model=schemas.PaymentSheetOut)
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

    payment_sheet = await StripeService.create_payment_sheet(
        user_id=token_payload.sub,
        customer_email=token_payload.email,
        price=total_price,
    )

    payment = schemas.PaymentCreate(
        payment_intent_id=payment_sheet.payment_intent_id,
        client_secret=payment_sheet.client_secret,
        customer_id=payment_sheet.customer_id,
        user_id=token_payload.sub,
        apartment_id=payload.apartment_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        price=total_price,
    )
    PaymentServices.create_payment(db, payment)

    message = {
        **payment_sheet.dict(),
        "user_id": token_payload.sub,
        "apartment_id": payload.apartment_id,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "price": total_price,
    }
    logging.info(f"Payment intent created. {message}.")

    return payment_sheet


@router.post("/webhook")
async def webhook_received(
    db: Session = Depends(get_db),
    *,
    request: Request,
    stripe_signature: str = Header(),
):
    data = await request.body()
    event = StripeService.construct_event(data, stripe_signature)

    logging.info(f"Received {event['type']} event.")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        await PaymentServices.confirm_payment(db, payment_intent["id"])

    return {"status": "success"}
