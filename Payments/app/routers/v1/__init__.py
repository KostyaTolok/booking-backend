from fastapi import APIRouter

from app.routers.v1.payment import router as payment_router
from app.routers.v1.booking import router as booking_router

router = APIRouter()

router.include_router(payment_router, prefix="/payment")

router.include_router(booking_router, prefix="/booking")
