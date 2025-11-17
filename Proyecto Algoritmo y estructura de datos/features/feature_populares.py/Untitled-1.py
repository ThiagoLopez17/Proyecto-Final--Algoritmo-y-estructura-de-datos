# features/feature_populares.py
from .db_connection import get_connection

def listar_populares():
    conn, kind = get_connection()
    cur = conn.cursor()
    if kind == "mysql":
        cur.execute("SELECT titulo, calificacion FROM libros WHERE calificacion >= 4 ORDER BY calificacion DESC")
        rows = cur.fetchall()
    else:
        cur.execute("SELECT titulo, calificacion FROM libros WHERE calificacion >= 4 ORDER BY calificacion DESC")
        rows = [(r["titulo"], r["calificacion"]) for r in cur.fetchall()]
    cur.close()
    if kind == "mysql":
        conn.close()
    else:
        conn.close()
    return rows
