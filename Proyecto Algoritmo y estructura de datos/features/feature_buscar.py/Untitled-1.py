# features/feature_buscar.py
from .db_connection import get_connection

def seleccionar_todos_los_libros():
    conn, kind = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM libros ORDER BY titulo")
    rows = cur.fetchall()
    if kind == "mysql":
        # filas tipo tuple
        libros = rows
    else:
        libros = [tuple(r) for r in rows]  # sqlite Row a tuple compatible
    cur.close()
    conn.close()
    return libros

def busqueda_binaria_libros(libros, titulo):
    inicio = 0
    fin = len(libros) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        titulo_medio = libros[medio][1]
        if titulo_medio == titulo:
            return libros[medio]
        elif titulo_medio < titulo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None

def buscar_por_titulo(titulo):
    libros = seleccionar_todos_los_libros()
    return busqueda_binaria_libros(libros, titulo)
