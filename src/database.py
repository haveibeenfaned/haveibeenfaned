import json
import logging
import os
import sys
from typing import Union

import psycopg
from psycopg.rows import dict_row

from src.models import Profile

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234") # .gitignore

logger = logging.getLogger(name="database")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("database.log")

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def save_profile(profile: Profile) -> Union[Profile, bool]:
    try:
        with psycopg.connect(host=host, dbname=dbname, user=user, password=password, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                if profile_exists(profile.handle, cursor):
                    update_sql("profiles", cursor, **profile.__dict__)
                else:
                    insert_sql("profiles", cursor, **profile.__dict__)

            conn.commit()

    except psycopg.Error as e:
        print(e)
        return False

    return profile


def insert_sql(table: str, cursor: psycopg.Cursor, **kwargs) -> bool:
    columns = ",".join(list(kwargs.keys()))
    values = list(map(lambda x: f"'{x}'" if x is not None else "NULL", list(kwargs.values())))
    values = ",".join(values)
    cursor.execute(f"INSERT INTO {table} ({columns}, created_at) VALUES ({values}, now())")  # add created at

    return True


def update_sql(table: str, cursor: psycopg.Cursor, **kwargs) -> bool:
    query = f"UPDATE {table} SET"
    for x, y in zip(kwargs.keys(), kwargs.values()):

        if x == "handle": continue

        y = f"'{y}'" if y is not None else "NULL"
        query += f" {x} = {y}, "

    query += " updated_at = now() "  # add updated_at
    query += " WHERE handle = '{}'".format(kwargs["handle"])

    cursor.execute(query)

    return True


def profile_exists(handle: str, cursor: psycopg.Cursor) -> bool:
    cursor.execute(f"SELECT * FROM profiles WHERE handle = '{handle}'")
    res = cursor.fetchone()

    if res:
        return True
    return False


def notify_back(res: dict) -> bool:
    logger.info(f"Database - Notify Back: {res}")
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"NOTIFY responses, '{json.dumps(res)}'")
        connection.commit()
    return True