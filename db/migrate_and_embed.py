#!/usr/bin/env python3
"""Run schema migration and populate embeddings directly against Supabase.

Usage:
    DB_HOST=aws-0-eu-west-1.pooler.supabase.com \
    DB_USER=postgres.zblomnipdfufnuvglsvw \
    DB_NAME=postgres \
    DB_PASSWORD=<password> \
    DB_PORT=5432 \
    OPENAI_API_KEY=<key> \
    python -m db.migrate_and_embed
"""
from openai import OpenAI
from db.connection import get_connection
import os

MIGRATION_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE profile ADD COLUMN IF NOT EXISTS embedding vector(1536);
CREATE INDEX IF NOT EXISTS profile_embedding_idx
    ON profile USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);
"""

def run():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    conn = get_connection()
    cur = conn.cursor()

    print("Running migration...")
    cur.execute(MIGRATION_SQL)
    conn.commit()
    print("Migration done.")

    cur.execute("SELECT id, category, label, detail FROM profile WHERE embedding IS NULL")
    rows = cur.fetchall()
    print(f"Embedding {len(rows)} profile rows...")

    for id, category, label, detail in rows:
        text = f"{category}: {label}. {detail or ''}"
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        embedding = response.data[0].embedding
        embedding_str = '[' + ','.join(map(str, embedding)) + ']'
        cur.execute("UPDATE profile SET embedding = %s::vector WHERE id = %s", (embedding_str, id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Done. {len(rows)} rows embedded.")

if __name__ == "__main__":
    run()
