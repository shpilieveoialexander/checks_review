from redis import Redis

from .settings import settings

jwt_blacklist = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def block_jwt_token(
    jwt_token: str, expired: int = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
) -> None:
    """Block JWT token on their expiry date"""
    jwt_blacklist.set(jwt_token, "", ex=expired * 60)
    return
