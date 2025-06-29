
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.app import app as finder

url_router = APIRouter()


@url_router.post("/{url}")
async def scan_url(url: str) -> JSONResponse:
    res = finder(url)

    if not url:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=url)

    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=res)
