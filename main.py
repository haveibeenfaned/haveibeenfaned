import uvicorn

from api.app import app

# fastapi dev / prod runs this imported app
# TODO: Fix frontend for different kind of responses from API
# TODO: Fix API for different kind of responses from Crawler