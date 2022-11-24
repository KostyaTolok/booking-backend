import asyncio
import logging
from decimal import Decimal
from typing import List

from async_stripe import stripe

from app import schemas
from app.core import exceptions
from app.core.config import config

stripe.api_key = config.STRIPE_SECRET_KEY


class StripeService:
    @staticmethod
    async def create_customer(user_id: int):
        customer = await stripe.Customer.create(idempotency_key=str(user_id))
        ephemeral_key = await stripe.EphemeralKey.create(
            customer=customer.id,
            stripe_version="2022-08-01",
        )
        return customer, ephemeral_key

    @staticmethod
    async def create_payment_intent(
        customer_id: int,
        customer_email: str,
        price: Decimal,
    ):
        return await stripe.PaymentIntent.create(
            amount=int(price * 100),
            currency="usd",
            customer=customer_id,
            receipt_email=customer_email,
            automatic_payment_methods={
                "enabled": True,
            },
        )

    @staticmethod
    async def crete_payment_sheet(
        user_id: int,
        customer_email: str,
        price: Decimal,
    ) -> schemas.PaymentSheet:
        customer, ephemeral_key = await StripeService.create_customer(
            user_id=user_id,
        )
        payment_intent = await StripeService.create_payment_intent(
            customer_id=customer.id,
            customer_email=customer_email,
            price=price,
        )
        return schemas.PaymentSheet(
            payment_intent_id=payment_intent.id,
            client_secret=payment_intent.client_secret,
            ephemeral_key=ephemeral_key.secret,
            customer_id=customer.id,
            publishable_key=config.STRIPE_PUBLISHABLE_KEY,
        )

    @staticmethod
    def construct_event(
        payload: bytes,
        signature: str,
    ):
        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=signature,
                secret=config.STRIPE_WEBHOOK_SECRET,
            )
        except ValueError as e:
            logging.info(f"Webhook invalid payload. {payload}")
            raise exceptions.BadRequestException(
                message="Webhook invalid payload",
            )
        except stripe.error.SignatureVerificationError as e:
            logging.info(f"Webhook invalid signature.")
            raise exceptions.BadRequestException(
                message="Invalid signature",
            )
        return event

    @staticmethod
    async def cancel_payment_intent(payment_intent_id: str):
        await stripe.PaymentIntent.cancel(payment_intent_id)

    @staticmethod
    async def batch_cancel_payment_intents(payment_intent_ids: List[str]):
        stripe_tasks = []
        for payment_intent_id in payment_intent_ids:
            stripe_future = StripeService.cancel_payment_intent(payment_intent_id)
            stripe_tasks.append(stripe_future)
        await asyncio.gather(*stripe_tasks)
