import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "jdanalyzer_db"),
        user=os.getenv("DB_USER", "jdanalyzer"),
        password=os.getenv("DB_PASSWORD", "123456789"),
    )