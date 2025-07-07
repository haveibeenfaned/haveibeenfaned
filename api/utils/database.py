import json
import os
import time
import psycopg

from src.models import Profile

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


def send_message(handle: str):
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True) as conn:

        with conn.cursor() as cursor:
            cursor.execute(f"NOTIFY requests, '{handle}'")
            c = 0

            cursor.execute("LISTEN responses")
            for res in conn.notifies(timeout=None):
                print(res)
                as_dict = json.loads(res.payload)

                if as_dict["isException"]:
                    profile = Profile(ig_url="", handle=handle)
                else:
                    profile = Profile(**as_dict["profile"])

                if profile.handle == handle:
                    return as_dict

                if c == 100:
                    return False

                time.sleep(1)
                c =+ 1
