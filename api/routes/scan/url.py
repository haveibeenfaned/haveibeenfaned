from http.client import OK, BAD_REQUEST, INTERNAL_SERVER_ERROR

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.app import app as finder

url_router = APIRouter()


@url_router.get("/scan/url")
async def scan_url(url: str) -> JSONResponse:
    res = finder(url)

    if not url:
        return JSONResponse(status_code=BAD_REQUEST, content=url)

    if res:
        return JSONResponse(status_code=OK, content=res)

    return JSONResponse(status_code=INTERNAL_SERVER_ERROR, content=res)
