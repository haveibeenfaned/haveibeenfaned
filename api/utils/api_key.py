import os
from http.client import HTTPException
from typing import Union

from fastapi import Security, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(api_key_header)) -> Union[bool, JSONResponse]:
    if api_key in os.getenv("APIKEY", "TEST"):
        return True
    else:
        raise HTTPException()

