import os
from typing import Union

from fastapi import Security, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-KEY")


def verify_api_key(api_key: str = Security(api_key_header)) -> Union[bool, JSONResponse]:
    if api_key in os.getenv("API_KEY", "TEST"):
        return True
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Invalid API Key"})
