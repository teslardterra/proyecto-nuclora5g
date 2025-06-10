import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

def seleccionar_db():
    """Abre un cuadro de diálogo para seleccionar el archivo .db"""
    archivo_db = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
    if archivo_db:
        entrada_db.delete(0, tk.END)
        entrada_db.insert(0, archivo_db)
        cargar_datos()

def cargar_datos():
    """Carga los datos de la base de datos seleccionada y los muestra en la tabla"""
    archivo_db = entrada_db.get()
    if not archivo_db:
        messagebox.showwarning("Advertencia", "Seleccione un archivo .db")
        return

    try:
        conn = sqlite3.connect(archivo_db)
        cursor = conn.cursor()

        # Obtener el nombre de la primera tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        if not tablas:
            messagebox.showerror("Error", "No se encontraron tablas en la base de datos")
            return

        nombre_tabla = tablas[0][0]  # Usar la primera tabla encontrada
        cursor.execute(f"SELECT * FROM {nombre_tabla}")

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Limpiar la tabla antes de insertar nuevos datos
        tree.delete(*tree.get_children())

        # Configurar encabezados en la tabla
        tree["columns"] = columnas
        tree["show"] = "headings"

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Insertar datos en la tabla
        for fila in cursor.fetchall():
            tree.insert("", tk.END, values=fila)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al leer la base de datos:\n{e}")

# Configurar la ventana principal
root = tk.Tk()
root.title("Visor de SQLite")

# Frame superior para seleccionar el archivo
frame_superior = tk.Frame(root)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Archivo DB:").pack(side=tk.LEFT, padx=5)
entrada_db = tk.Entry(frame_superior, width=50)
entrada_db.pack(side=tk.LEFT, padx=5)
tk.Button(frame_superior, text="Seleccionar", command=seleccionar_db).pack(side=tk.LEFT, padx=5)

# Frame para contener la tabla y la barra de desplazamiento
frame_tabla = tk.Frame(root)
frame_tabla.pack(expand=True, fill="both")

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Tabla para mostrar datos
tree = ttk.Treeview(frame_tabla, yscrollcommand=scrollbar.set)
tree.pack(expand=True, fill="both", side="left")

scrollbar.config(command=tree.yview)

# Botón para cargar datos manualmente
tk.Button(root, text="Cargar Datos", command=cargar_datos).pack(pady=5)

# Ejecutar la aplicación
root.mainloop()
