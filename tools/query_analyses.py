from db.connection import get_connection

def query_analyses(filter_sql=None):
    conn = get_connection()
    cur = conn.cursor()

    if filter_sql:
        cur.execute(f"SELECT * FROM analyses WHERE {filter_sql}")
    else:
        cur.execute("SELECT * FROM analyses")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows