# app.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from features.feature_populares import listar_populares
from features.feature_agregar import agregar_libro_interactivo
from features.feature_eliminar import listar_y_eliminar_libro
from features.feature_buscar import buscar_por_titulo

# Ventana principal
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca - Interfaz (GLHF)")
        self.geometry("800x500")
        self._create_widgets()

    def _create_widgets(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        ttk.Label(top, text="Biblioteca - Panel de control", font=("Segoe UI", 14)).pack(side="left")

        # Frame de botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=6)

        ttk.Button(btn_frame, text="Listar libros populares", command=self.on_listar_populares).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Agregar libro", command=self.on_agregar_libro).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Eliminar libro", command=self.on_eliminar_libro).pack(side="left", padx=6)

        # Buscador
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=8)
        ttk.Label(search_frame, text="Buscar por título:").pack(side="left", padx=(0,6))
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left")
        ttk.Button(search_frame, text="Buscar", command=self.on_buscar).pack(side="left", padx=6)

        # Output
        out_frame = ttk.Frame(self)
        out_frame.pack(fill="both", expand=True, padx=10, pady=8)
        self.txt = tk.Text(out_frame, wrap="word")
        self.txt.pack(fill="both", expand=True)

    def log(self, text):
        self.txt.insert("end", str(text) + "\n")
        self.txt.see("end")

    # Callbacks
    def on_listar_populares(self):
        try:
            rows = listar_populares()
            if not rows:
                self.log("No hay libros con calificación >= 4.")
                return
            self.log("Libros populares (calificación >= 4):")
            for r in rows:
                self.log(f" - {r[0]} — calificación: {r[1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al listar: {e}")

    def on_agregar_libro(self):
        try:
            agrego = agregar_libro_interactivo(parent=self)
            if agrego:
                self.log(f"Libro agregado: {agrego}")
            else:
                self.log("Alta cancelada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar: {e}")

    def on_eliminar_libro(self):
        try:
            resultado = listar_y_eliminar_libro(parent=self)
            if resultado:
                self.log(f'Eliminado: {resultado}')
            else:
                self.log("No se eliminó ningún libro.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def on_buscar(self):
        titulo = self.search_var.get().strip()
        if not titulo:
            messagebox.showinfo("Buscar", "Ingresa un título para buscar.")
            return
        try:
            res = buscar_por_titulo(titulo)
            if res:
                self.log(f"Libro encontrado: {res}")
            else:
                self.log("Libro no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en la búsqueda: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
