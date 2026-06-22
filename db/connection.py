import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "jdanalyzer_db"),
        user=os.getenv("DB_USER", "jdanalyzer"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", None),
        port=os.getenv("DB_PORT", "5432")
    )