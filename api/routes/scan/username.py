from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.utils.database import send_message

username_router = APIRouter()


@username_router.post("/{username}")
async def scan_username(username: str) -> JSONResponse:
    res = await send_message(username)

    return JSONResponse(status_code=res["status_code"], content=res)
