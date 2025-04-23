import logging

from fastapi import FastAPI
from api.routes.scan.url import url_router
from api.routes.scan.username import username_router

logger = logging.getLogger("app.txt")
app = FastAPI()
app.include_router(url_router)
app.include_router(username_router)