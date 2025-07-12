import json
import os

import psycopg

from src.models import Profile

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


async def send_message(handle: str):
    aconn = await psycopg.AsyncConnection.connect(host=host, dbname=dbname, user=user, password=password,
                                               autocommit=True)
    async with aconn:
        async with aconn.cursor() as cursor:

            await cursor.execute(f"NOTIFY requests, '{handle}'")
            await cursor.execute("LISTEN responses")

            async for res in aconn.notifies():
                print(res)
                as_dict = json.loads(res.payload)

                if as_dict["isException"]:
                    profile = Profile(ig_url="", handle=handle)
                else:
                    profile = Profile(**as_dict["profile"])

                if profile.handle == handle:
                    return as_dict

                return None
            return None