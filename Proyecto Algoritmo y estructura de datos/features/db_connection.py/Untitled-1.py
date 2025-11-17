# features/db_connection.py
import os
import sqlite3

# Intentar mysql, si no usar sqlite
try:
    import mysql.connector as mysql_connector
    MYSQL_AVAILABLE = True
except Exception:
    MYSQL_AVAILABLE = False

# Configuración por defecto (ajustar si usás MySQL)
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "biblioteca"
}

SQLITE_DB = os.path.join(os.path.dirname(__file__), "..", "biblioteca_local.db")


def get_connection():
    """
    Devuelve una conexión. Prioriza MySQL si está disponible y la DB existe.
    Si no, crea/usa sqlite local.
    """
    if MYSQL_AVAILABLE:
        try:
            conn = mysql_connector.connect(**MYSQL_CONFIG)
            return conn, "mysql"
        except Exception:
            # fallback a sqlite
            pass

    # sqlite
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"