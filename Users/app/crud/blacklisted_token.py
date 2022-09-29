from typing import Any, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.token import BlacklistedToken
from app.schemas.token import BlacklistedTokenCreate


class CRUDUser(CRUDBase[BlacklistedToken, BlacklistedTokenCreate, BlacklistedTokenCreate]):
    def get_by_jti(self, db: Session, *, jti: Any) -> Optional[BlacklistedToken]:
        return db.query(BlacklistedToken).filter(BlacklistedToken.jti == jti).first()


blacklisted_token = CRUDUser(BlacklistedToken)
