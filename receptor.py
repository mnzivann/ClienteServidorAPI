import tkinter as tk
from tkinter import ttk
import requests

API_MESSAGES = "http://localhost:8080/api/clienteservidor/messages"
API_USERS = "http://localhost:8080/api/clienteservidor/users"

def update_monitor():
    try:
        # 1. Actualizar Mensajes
        res_msg = requests.get(API_MESSAGES)
        if res_msg.status_code == 200:
            messages = res_msg.json()
            listbox_messages.delete(0, tk.END)
            for msg in messages:
                listbox_messages.insert(tk.END, f" [{msg['sender']}]: {msg['text']}")

        # 2. Actualizar Base de Datos de Usuarios
        res_usr = requests.get(API_USERS)
        if res_usr.status_code == 200:
            users = res_usr.json()
            listbox_users.delete(0, tk.END)
            for user in users:
                listbox_users.insert(tk.END, f" {user}")
    except:
        pass
    
    # Ciclo de consulta automatica cada 2 segundos
    root.after(2000, update_monitor)

# Configuracion de Ventana Principal
root = tk.Tk()
root.title("Servidor - Panel de Monitoreo")
root.geometry("700x400")
root.configure(bg="#F3F4F6")

# Layout de dos columnas
frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)

frame_right = tk.Frame(root, bg="#F3F4F6")
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 20), pady=20)
# Columna Izquierda: Mensajes
tk.Label(frame_left, text="Historial de Comunicacion", font=("Arial", 12, "bold"), bg="#F3F4F6", fg="#1F2937").pack(anchor=tk.W, pady=(0, 5))
container_msg = tk.Frame(frame_left, bg="#FFFFFF", bd=1, relief="solid")
container_msg.pack(fill=tk.BOTH, expand=True)

listbox_messages = tk.Listbox(container_msg, font=("Arial", 11), borderwidth=0, highlightthickness=0, bg="#FFFFFF", fg="#374151")
listbox_messages.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Columna Derecha: Base de Datos de Usuarios
tk.Label(frame_right, text="Usuarios en DB", font=("Arial", 12, "bold"), bg="#F3F4F6", fg="#1F2937").pack(anchor=tk.W, pady=(0, 5))
container_usr = tk.Frame(frame_right, bg="#FFFFFF", bd=1, relief="solid")
container_usr.pack(fill=tk.BOTH, expand=True)

listbox_users = tk.Listbox(container_usr, font=("Arial", 11), borderwidth=0, highlightthickness=0, bg="#FFFFFF", fg="#374151")
listbox_users.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Iniciar sincronizacion automatica
update_monitor()
root.mainloop()