"""
db.py – Database connection helper for StudyTrack.
Uses mysql-connector-python with a retry loop so the app waits
for MySQL to become ready inside Docker.
"""

import os
import time
import mysql.connector
from mysql.connector import Error


def get_db_config():
    """Read DB connection settings from environment variables."""
    return {
        "host": os.getenv("MYSQL_HOST", "db"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "user": os.getenv("MYSQL_USER", "studytrack"),
        "password": os.getenv("MYSQL_PASSWORD", "studytrack123"),
        "database": os.getenv("MYSQL_DATABASE", "studytrack"),
    }


def get_connection(retries=10, delay=3):
    """
    Return a MySQL connection. Retries up to `retries` times with
    `delay` seconds between attempts (useful during container startup).
    """
    config = get_db_config()
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(**config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"[DB] Attempt {attempt}/{retries} – {e}")
            if attempt < retries:
                time.sleep(delay)
    raise Exception("Could not connect to MySQL after multiple retries.")


def execute_query(query, params=None, fetch=False, commit=False):
    """
    Helper: run a query, optionally fetch results or commit changes.
    Always closes the connection after use.
    Returns:
      - list of dicts  if fetch=True
      - lastrowid      if commit=True
      - None            otherwise
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        if commit:
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()
