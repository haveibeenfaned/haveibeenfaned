import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support

import psycopg
from psycopg import Notify

from src.app import app

# local crawler session
# requires proxied POSTGRESQL connection for production run

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


async def main() -> True:
    # LOCKER
    try:
        loop = asyncio.get_event_loop()
        tasks = []

        # TODO: This is still running on the main loop thus it only listens one at a time?
        conn = await psycopg.AsyncConnection.connect(host=host, dbname=dbname, user=user, password=password,
                                                     autocommit=True)
        async with conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE status SET status = true WHERE process = 'CRAWLER'")

        with ProcessPoolExecutor(max_workers=10) as executor:
            async with conn:
                async with conn.cursor() as cursor2:
                    await cursor2.execute("LISTEN requests;")
                    print("Listening...")
                    async for request in conn.notifies(timeout=None):
                        print(request)
                        request: Notify = request
                        tasks.append(loop.run_in_executor(executor, app, request.payload))

    except (Exception, BaseException) as err:
        print("Ran into an error / interrupt, shutting down")
        print(err)
        async with conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE status SET status = false WHERE process = 'CRAWLER'")
                await cursor.execute("NOTIFY responses, ''")  # TODO: Add exception response here

        return None


if __name__ == '__main__':
    freeze_support()
    asyncio.run(main())
