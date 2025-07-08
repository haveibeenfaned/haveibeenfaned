import json
import os

import psycopg
from psycopg import Notify

from src.app import app

# local crawler session
# requires proxied POSTGRESQL connection for production run

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


def main():
    try:

        conn = psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True)
        cursor = conn.cursor()
        cursor.execute("UPDATE status SET status = true WHERE process = 'CRAWLER'")

        conn2 = psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True)
        cursor2 = conn2.cursor()
        cursor.execute("LISTEN requests;")

        for request in conn.notifies(timeout=None):
            print(request)
            request: Notify = request
            res = app(str(request.payload))

            cursor2.execute(f"NOTIFY responses, '{json.dumps(res)}';")
            conn2.commit()
    except (Exception, BaseException) as err:
        print("Ran into an error / interrupt, shutting down")
        conn = psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True)
        cursor = conn.cursor()
        cursor.execute("UPDATE status SET status = false WHERE process = 'CRAWLER'")
        cursor.execute("NOTIFY responses, ''")


if __name__ == "__main__":
    main()
