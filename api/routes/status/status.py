import logging
import os

import psycopg
from fastapi import APIRouter, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse

status_router = APIRouter()


@status_router.get("/database")
async def database_status() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content=str(get_status("DATABASE")))


@status_router.get("/crawler")
async def crawler_status() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content=str(get_status("CRAWLER")))


def get_status(process: str) -> bool:
    try:
        with psycopg.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "1234"),
                dbname=os.getenv("DB_DATABASE", "postgres")
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT status FROM status WHERE process = '{process}'")
                res = cur.fetchall()
                logger.info(f"Status: {res}")

                if res[0][0]: return True

    except Exception as e:
        logging.warning(f"Database error, {e}")

    return False


__all__ = ["status_router"]
