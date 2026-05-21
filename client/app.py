import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:8080/api/techdash/tasks"

def fetch_tasks():
    try:
        # Consumir la API REST
        response = requests.get(API_URL)
        response.raise_for_status()
        tasks = response.json()
        
        # Limpiar la lista actual
        listbox.delete(0, tk.END)
        
        # Poblar la interfaz con los datos
        for task in tasks:
            status_icon = "✓" if task['status'] == "Completado" else "✗"
            listbox.insert(tk.END, f"[{status_icon}] {task['title']}")
            
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor Go:\n{e}")

# Configuración de la Ventana Principal
root = tk.Tk()
root.title("TechDash - Interfaz de Técnico")
root.geometry("450x300")
root.configure(padx=20, pady=20)

# Elementos de la UI
header = tk.Label(root, text="Panel de Tareas", font=("Arial", 16, "bold"))
header.pack(pady=(0, 10))

btn = tk.Button(root, text="Sincronizar Tareas", command=fetch_tasks, bg="#0078D7", fg="white")
btn.pack(fill=tk.X, pady=5)

listbox = tk.Listbox(root, font=("Consolas", 11), height=10)
listbox.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()