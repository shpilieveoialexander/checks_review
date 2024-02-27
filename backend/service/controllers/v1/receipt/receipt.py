from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from db import models
from db.session import DBSession
from service.core.dependencies import get_current_user, get_session
from service.core.filters import apply_search
from service.schemas import v1 as schemas_v1

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas_v1.Receipt
)
async def create_recept(
    input_data: schemas_v1.ReceiptCreate,
    session: DBSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create receipt\n
    Obtain input data and return new receipt\n
    Responses:\n
    `201` CREATED - Everything is good (SUCCESS Response)\n
    `401` UNAUTHORIZED - You have not provided authorization token\n
    `422` UNPROCESSABLE_ENTITY - Failed field validation\n
    """
    receipt = models.Receipt(
        user_id=current_user.id, type=input_data.type, total=input_data.amount
    )

    with session() as db:
        db.add(receipt)
        db.flush()

        total = 0
        for product_data in input_data.product:
            product = models.Product(name=product_data.name, price=product_data.price)
            db.add(product)
            db.flush()
            total += product_data.price * product_data.quantity
            position = models.Position(
                product_id=product.id,
                quantity=product_data.quantity,
                total_price=product_data.price * product_data.quantity,
                receipt_id=receipt.id,
            )
            db.add(position)
        receipt.total = total
        receipt.rest = input_data.amount - total
        db.commit()
        db.refresh(receipt)

    return receipt


@router.get("/", response_model=Page[schemas_v1.Receipt])
async def get_receipts(
    request: Request,
    session: DBSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    """
    Get User's receipt\n
    Responses:\n
    `200` OK - Everything is good (SUCCESS Response)\n
    `401` UNAUTHORIZED - You have not provided authorization token\n
    """
    query = session.query(models.Receipt).where(
        models.Receipt.user_id == current_user.id
    )
    receipts = paginate(
        apply_search(models.Receipt, query, query_params=request.query_params)
    )
    return receipts
