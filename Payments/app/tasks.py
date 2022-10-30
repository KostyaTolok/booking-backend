from fastapi_utils.tasks import repeat_every

from app.core.config import config
from app.core.db import SessionLocal
from app.crud.payment import PaymentCRUD
from app.services.stripe import StripeService


@repeat_every(
    seconds=config.REMOVE_EXPIRED_PAYMENT_INTENTS_SECONDS, raise_exceptions=True
)
async def remove_expired_payment_intents():
    with SessionLocal() as db:
        payment_intents = PaymentCRUD.get_expired(db)

        payment_intent_stripe_ids = [p.payment_intent_id for p in payment_intents]
        await StripeService.batch_cancel_payment_intents(payment_intent_stripe_ids)

        payment_intent_db_ids = [p.id for p in payment_intents]
        PaymentCRUD.batch_delete(db, payment_intent_db_ids)
