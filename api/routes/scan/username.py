from http.client import OK, BAD_REQUEST, INTERNAL_SERVER_ERROR

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.app import app as finder

username_router = APIRouter()


@username_router.get("/scan/username")
async def scan_username(username: str) -> JSONResponse:
    res = finder(f"https://www.instagram.com/{username}/?hl=en")

    if not username:
        return JSONResponse(status_code=BAD_REQUEST, content=username)

    if res:
        return JSONResponse(status_code=OK, content=res)

    return JSONResponse(status_code=INTERNAL_SERVER_ERROR, content=res)
