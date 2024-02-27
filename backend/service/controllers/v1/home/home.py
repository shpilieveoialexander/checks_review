from typing import Dict

from fastapi import APIRouter, Request

from db.session import DBSession
from service.core import settings
from service.schemas import v1 as schemas_v1

router = APIRouter()


@router.get("/", response_model=schemas_v1.HomeResponse)
async def home(request: Request) -> Dict[str, Dict[str, str]]:
    return {
        "backend_status": {
            "message": "Backend service is working",
            "current_version": f"v{settings.VERSION}",
            "redoc": f"http://{settings.SERVER_HOST}/redoc",
            "swagger": f"http://{settings.SERVER_HOST}/docs",
        },
        "db_status": {
            "message": f"DB service {'has' if DBSession else 'has not'} been started",
            "adminer": f"http://{settings.SERVER_HOST}/adminer",
        },
    }
