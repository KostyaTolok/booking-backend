from pydantic import BaseModel


class PaymentSheet(BaseModel):
    payment_intent: str
    ephemeral_key: str
    customer: str
    publishable_key: str
