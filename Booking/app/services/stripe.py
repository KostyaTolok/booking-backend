import asyncio
from decimal import Decimal
from typing import List

from async_stripe import stripe

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
            currency="eur",
            customer=customer_id,
            receipt_email=customer_email,
            automatic_payment_methods={
                "enabled": True,
            },
        )

    @staticmethod
    async def construct_event(
        payload: bytes,
        signature: str,
    ):
        return await stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=config.STRIPE_WEBHOOK_SECRET,
        )

    @staticmethod
    async def cancel_payment_intent(payment_intent_id: str):
        stripe.PaymentIntent.cancel(
            payment_intent_id,
        )

    @staticmethod
    async def batch_cancel_payment_intents(payment_intent_ids: List[str]):
        stripe_tasks = []
        for payment_intent_id in payment_intent_ids:
            stripe_future = StripeService.cancel_payment_intent(payment_intent_id)
            stripe_tasks.append(stripe_future)
        await asyncio.gather(*stripe_tasks)
