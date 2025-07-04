import psycopg
import time


with psycopg.connect(host='localhost', dbname='postgres', user='postgres', password='1234', autocommit=True) as conn:
    connection: psycopg.Connection = conn
    cursor = connection.cursor()

    cursor.execute("LISTEN requests")
    print("SQL Executed, starting to listen")
    gen = connection.notifies(timeout=5)
    for message in connection.notifies(timeout=None):
        time.sleep(5)
        message: psycopg.Notify = message

        print("Message was: " + str(message))
