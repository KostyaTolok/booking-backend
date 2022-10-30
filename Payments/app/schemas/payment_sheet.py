from pydantic import BaseModel


class PaymentSheet(BaseModel):
    payment_intent_id: str
    ephemeral_key: str
    customer_id: str
    publishable_key: str
