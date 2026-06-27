#!/usr/bin/env python3
"""Run once after schema migration to generate and store embeddings for all profile rows."""
from openai import OpenAI
from db.connection import get_connection
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_profile():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, category, label, detail FROM profile")
    rows = cur.fetchall()

    for id, category, label, detail in rows:
        text = f"{category}: {label}. {detail or ''}"
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        embedding = response.data[0].embedding
        embedding_str = '[' + ','.join(map(str, embedding)) + ']'
        cur.execute("UPDATE profile SET embedding = %s::vector WHERE id = %s", (embedding_str, id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Embedded {len(rows)} profile rows.")

if __name__ == "__main__":
    embed_profile()
