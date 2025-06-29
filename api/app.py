import logging
import os

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.scan.url import url_router
from api.routes.scan.username import username_router
from api.utils.api_key import verify_api_key
from fastapi.staticfiles import StaticFiles

logger = logging.Logger("app-logger")
app = FastAPI()
app.include_router(url_router, prefix="/api/v1/scan/url", dependencies=[Depends(verify_api_key)])
app.include_router(username_router, prefix="/api/v1/scan/username")
origins = os.getenv("ORIGINS", ["http://localhost", "http://localhost:3000"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory='./ui', html=True), name="web")


@app.get("/api")
async def index():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "haveibeenfaned API V1"})