from app import db
import psycopg2
from os import getenv

def get_db_connection():
    return psycopg2.connect(getenv("DATABASE_URL"))

def execute_sql(filepath):
    with open(filepath, 'r') as file:
        sql_commands = file.read()

    conn = get_db_connection()
    cur = conn.cursor()
    for command in sql_commands.split(';'):
        command = command.strip()
        if command:
            cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()

def execute_query(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def execute_modify(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()
