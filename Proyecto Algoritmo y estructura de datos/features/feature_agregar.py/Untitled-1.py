# features/feature_agregar.py
from datetime import datetime
from .db_connection import get_connection
import tkinter as tk
from tkinter import simpledialog, messagebox

def agregar_libro(titulo, autor, genero, publicacion, cantidad, calificacion):
    conn, kind = get_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO libros (titulo, autor, genero, publicacion, cantidad_disponible, calificacion)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    vals = (titulo, autor, genero, publicacion, cantidad, calificacion)
    if kind == "sqlite":
        sql = sql.replace("%s", "?")
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()
    return True

def agregar_libro_interactivo(parent=None):
    """
    Abre dialogs para pedir datos al usuario (usado por la GUI).
    Devuelve el título agregado o None si canceló.
    """
    root = parent or tk._get_default_root()
    titulo = simpledialog.askstring("Agregar libro", "Título:", parent=root)
    if not titulo:
        return None
    autor = simpledialog.askstring("Agregar libro", "Autor:", parent=root) or ""
    genero = simpledialog.askstring("Agregar libro", "Género:", parent=root) or ""
    fecha = simpledialog.askstring("Agregar libro", "Fecha (YYYY-MM-DD):", parent=root) or datetime.today().strftime("%Y-%m-%d")
    try:
        cantidad = int(simpledialog.askstring("Agregar libro", "Cantidad disponible:", parent=root) or "1")
    except ValueError:
        cantidad = 1
    try:
        calificacion = int(simpledialog.askstring("Agregar libro", "Calificación (1-5):", parent=root) or "3")
    except ValueError:
        calificacion = 3

    try:
        agregar_libro(titulo, autor, genero, fecha, cantidad, calificacion)
        messagebox.showinfo("Agregar libro", f"Libro '{titulo}' agregado correctamente.", parent=root)
        return titulo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el libro: {e}", parent=root)
        return None
