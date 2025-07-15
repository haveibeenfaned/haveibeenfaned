import asyncio
import http.client
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support

import psycopg
from psycopg import Notify

from database import notify_back
from src.app import app, create_payload
from src.models import Profile

# local crawler session
# requires proxied POSTGRESQL connection for production run

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


def main() -> True:
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()

        tasks = []
        conn = psycopg.connect(host=host, dbname=dbname, user=user, password=password,
                               autocommit=True)
        with conn.cursor() as cursor:
            cursor.execute("UPDATE status SET status = true WHERE process = 'CRAWLER'")

        with ProcessPoolExecutor(max_workers=10) as executor:
            with conn.cursor() as cursor2:
                cursor2.execute("LISTEN requests;")
                print("Listening...")
                for request in conn.notifies(timeout=None):
                    print(request)
                    request: Notify = request
                    # copy_profile(request.payload)
                    tasks.append(loop.run_in_executor(executor, app, request.payload))

    except (Exception, BaseException) as err:
        # TODO: Add exception response in notify, standarise a bit the exception flow
        print("Ran into an error / interrupt, shutting down")
        print(err)
        with conn.cursor() as cursor:
            cursor.execute("UPDATE status SET status = false WHERE process = 'CRAWLER'")

        return notify_back(
            create_payload(isException=False, exception="You have NOT been faned! He/She is for the streets",
                           status_code=http.client.INTERNAL_SERVER_ERROR, profile=Profile(handle=request.payload,
                                                                                          ig_url=f"https://www.instagram.com/{request.payload}").__dict__))

    return None


def copy_profile(handle: str):
    from shutil import copytree
    import pathlib
    abs_data_path = str(pathlib.Path().absolute()) + f"/.data/{handle}"

    abs_path = os.getenv("USERDATADIR", "")
    copytree(abs_path, abs_data_path)

    return True


if __name__ == '__main__':
    freeze_support()
    main()
