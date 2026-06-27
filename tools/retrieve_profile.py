from openai import OpenAI
from db.connection import get_connection
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def retrieve_profile(query_text, top_k=8):
    response = client.embeddings.create(model="text-embedding-3-small", input=query_text)
    embedding_str = '[' + ','.join(map(str, response.data[0].embedding)) + ']'

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT category, label, detail
        FROM profile
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (embedding_str, top_k))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"category": r[0], "label": r[1], "detail": r[2]} for r in rows]
