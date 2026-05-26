import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_MESSAGES = "http://localhost:8080/api/clienteservidor/messages"
API_USERS = "http://localhost:8080/api/clienteservidor/users"

def send_message():
    sender = entry_sender.get().strip()
    text = entry_message.get().strip()
    
    if not sender or not text:
        messagebox.showwarning("Campos vacios", "Por favor introduce tu nombre y el mensaje.")
        return

    try:
        payload = {"sender": sender, "text": text}
        response = requests.post(API_MESSAGES, json=payload)
        response.raise_for_status()
        
        entry_message.delete(0, tk.END)
        fetch_db_users() # Actualizar lista de usuarios local
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error de conexion: {e}")

def fetch_db_users():
    try:
        response = requests.get(API_USERS)
        if response.status_code == 200:
            users = response.json()
            listbox_users.delete(0, tk.END)
            for user in users:
                listbox_users.insert(tk.END, f"  {user}")
    except:
        pass

# Configuracion de UI Moderna
root = tk.Tk()
root.title("Cliente - Transmisor de Datos")
root.geometry("450x450")
root.configure(bg="#F3F4F6")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#F3F4F6", foreground="#1F2937", font=("Arial", 10))
style.configure("TButton", background="#4F46E5", foreground="white", font=("Arial", 10, "bold"), borderwidth=0)
style.map("TButton", background=[("active", "#4338CA")])

# Contenedor de Formulario
frame_form = tk.Frame(root, bg="#FFFFFF", bd=1, relief="solid", padx=15, pady=15)
frame_form.pack(fill=tk.X, padx=20, pady=15)

ttk.Label(frame_form, text="Nombre del Remitente", font=("Arial", 10, "bold")).pack(anchor=tk.W)
entry_sender = ttk.Entry(frame_form, font=("Arial", 11))
entry_sender.pack(fill=tk.X, pady=(5, 15))

ttk.Label(frame_form, text="Mensaje a Enviar", font=("Arial", 10, "bold")).pack(anchor=tk.W)
entry_message = ttk.Entry(frame_form, font=("Arial", 11))
entry_message.pack(fill=tk.X, pady=(5, 15))

btn_send = ttk.Button(frame_form, text="Enviar Registro", command=send_message)
btn_send.pack(fill=tk.X, ipady=4)

# Contenedor de Base de Datos de Usuarios
ttk.Label(root, text="Usuarios Registrados en Base de Datos", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=25)
frame_db = tk.Frame(root, bg="#FFFFFF", bd=1, relief="solid")
frame_db.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

listbox_users = tk.Listbox(frame_db, font=("Arial", 11), borderwidth=0, highlightthickness=0, bg="#FFFFFF", fg="#374151")
listbox_users.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

fetch_db_users()
root.mainloop()