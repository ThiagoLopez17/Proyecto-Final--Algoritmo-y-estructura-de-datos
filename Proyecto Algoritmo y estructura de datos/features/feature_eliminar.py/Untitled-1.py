# features/feature_eliminar.py
from .db_connection import get_connection
import tkinter as tk
from tkinter import simpledialog, messagebox

def listar_libros():
    conn, kind = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_libro, titulo FROM libros ORDER BY titulo")
    rows = cur.fetchall()
    if kind == "mysql":
        rows = [(r[0], r[1]) for r in rows]
    else:
        rows = [(r["id_libro"], r["titulo"]) for r in rows]
    cur.close()
    conn.close()
    return rows

def eliminar_libro_por_id(id_libro):
    conn, kind = get_connection()
    cur = conn.cursor()
    sql = "DELETE FROM libros WHERE id_libro = %s"
    if kind == "sqlite":
        sql = "DELETE FROM libros WHERE id_libro = ?"
    cur.execute(sql, (id_libro,))
    conn.commit()
    cur.close()
    conn.close()
    return True

def listar_y_eliminar_libro(parent=None):
    root = parent or tk._get_default_root()
    libros = listar_libros()
    if not libros:
        messagebox.showinfo("Eliminar libro", "No hay libros para eliminar.", parent=root)
        return None
    opciones = [f"{l[1]} (id:{l[0]})" for l in libros]
    seleccion = simpledialog.askinteger("Eliminar libro", 
                                        "Elige el número del libro a eliminar:\n" + "\n".join(f"{i+1}. {opciones[i]}" for i in range(len(opciones))),
                                        parent=root)
    if not seleccion or not (1 <= seleccion <= len(libros)):
        return None
    id_libro = libros[seleccion-1][0]
    titulo = libros[seleccion-1][1]
    eliminar_libro_por_id(id_libro)
    messagebox.showinfo("Eliminar libro", f"Eliminado: {titulo}", parent=root)
    return titulo
