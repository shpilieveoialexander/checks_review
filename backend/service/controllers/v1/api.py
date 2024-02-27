from fastapi import APIRouter
from fastapi_pagination import add_pagination

from .receipt import receipt
from .user import auth, user

router_v1 = APIRouter()

router_v1.include_router(auth.router, tags=["Auth"], prefix="/auth")
router_v1.include_router(user.router, tags=["User"], prefix="/user")
router_v1.include_router(receipt.router, tags=["Receipt"], prefix="/receipt")

add_pagination(router_v1)
