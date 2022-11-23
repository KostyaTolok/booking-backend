from app import crud
from app.core.utils.security.jwt import tokens


class AuthService:
    @staticmethod
    async def get_access_refresh_tokens(
        db, *, user_id: int, user_email: str, user_active: bool
    ) -> dict:
        access = tokens.AccessToken().for_user(subject=user_id)
        access["role"] = "user"
        access["active"] = user_active
        access["email"] = user_email

        last_token = crud.token.get_last_by_user_id(db, user_id=user_id)
        if last_token:
            tokens.RefreshToken(db, token=last_token, verify=False).blacklist()

        refresh = tokens.RefreshToken(db).for_user(subject=user_id)

        return {"access_token": str(access), "refresh_token": str(refresh)}

    @staticmethod
    async def refresh_tokens(db, *, refresh_token: str) -> dict:
        payload = tokens.RefreshToken(db, token=refresh_token)

        user = crud.user.get(db, payload["sub"])

        return await AuthService.get_access_refresh_tokens(
            db,
            user_id=user.id,
            user_email=user.email,
            user_active=user.is_active,
        )
