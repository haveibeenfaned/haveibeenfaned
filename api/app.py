import logging
import os

from api.routes.scan.username import username_router
from api.routes.status.status import status_router
from api.utils.api_key import verify_api_key
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

logger = logging.Logger("app-logger")
app = FastAPI(root_path="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(username_router, prefix="/scan/username")
app.include_router(status_router, prefix="/status")

origins = os.getenv("ORIGINS", ["http://localhost", "http://localhost:3000", "http://localhost:8001"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory='./ui', html=True), name="web")


@app.get("/api/")
async def index():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "haveibeenfaned API V1"})
