from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.app import app as finder

username_router = APIRouter()


@username_router.post("/{username}")
async def scan_username(username: str) -> JSONResponse:
    res = finder(f"https://www.instagram.com/{username}/?hl=en")
    print(res)
    if not username:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=username)
    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=res)
