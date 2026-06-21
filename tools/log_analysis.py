from db.connection import get_connection

def log_analysis(company, role, fit_score, missing_skills, source_url=None):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO analyses (company, role, fit_score, missing_skills, source_url)
        VALUES (%s, %s, %s, %s, %s)
    """, (company, role, fit_score, missing_skills, source_url))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {"status": "logged", "company": company, "role": role, "fit_score": fit_score}