from fastapi import APIRouter, Depends

from db import models
from service.core.dependencies import get_current_user
from service.schemas import v1 as schemas_v1

router = APIRouter()


@router.get("/me/", response_model=schemas_v1.User)
async def user_me(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    Return User me info\n
    Responses:\n
    `200` OK - Everything is good (SUCCESS Response)\n
    `401` UNAUTHORIZED - You have not provided authorization token\n
    `403` FORBIDDEN - Invalid authorization\n
    `422` UNPROCESSABLE_ENTITY - Failed field validation\n
    """
    return current_user
