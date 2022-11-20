from pydantic import BaseModel


class PaymentSheetBase(BaseModel):
    client_secret: str
    ephemeral_key: str
    customer_id: str
    publishable_key: str


class PaymentSheetOut(PaymentSheetBase):
    ...


class PaymentSheet(PaymentSheetBase):
    payment_intent_id: str
