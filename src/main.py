import os

import psycopg
from psycopg import Notify

from src.app import app

# local crawler session
# requires proxied POSTGRESQL connection for producton run

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


def main():
    conn = psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True)
    cursor = conn.cursor()

    conn2 = psycopg.connect(host=host, dbname=dbname, user=user, password=password, autocommit=True)
    cursor2 = conn2.cursor()

    for request in cursor.execute("LISTEN requests"):
        print(request)
        request: Notify = request
        res = app(str(request.payload))

        cursor2.execute(f"NOTIFY responses, {res}")
        conn2.commit()


if __name__ == "__main__":
    main()
