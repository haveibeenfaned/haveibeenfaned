from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.utils.database import send_message

username_router = APIRouter()


@username_router.post("/{username}")
async def scan_username(username: str) -> JSONResponse:
    res = await send_message(username)

    if not username:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=username)
    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=res)
