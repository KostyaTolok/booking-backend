from app.crud.base import CRUDBase
from app.models.token import BlacklistedToken
from app.schemas.token import BlacklistedTokenCreate


class CRUDBlacklistedToken(
    CRUDBase[BlacklistedToken, BlacklistedTokenCreate, BlacklistedTokenCreate]
):
    ...


blacklisted_token = CRUDBlacklistedToken(BlacklistedToken)
