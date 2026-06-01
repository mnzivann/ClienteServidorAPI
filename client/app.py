import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_MESSAGES = "http://localhost:8081/api/clienteservidor/messages"

def send_message():
    usuario = entry_user.get().strip()
    texto = entry_text.get().strip()
    
    if not usuario or not texto:
        messagebox.showwarning("Campos Vacíos", "Debes escribir tu nombre y un mensaje.")
        return

    try:
        requests.post(API_MESSAGES, json={"sender": usuario, "text": texto})
        entry_text.delete(0, tk.END)
        messagebox.showinfo("Éxito", "¡El mensaje fue entregado al servidor Go!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor Docker:\n{e}")

# --- INTERFAZ GRÁFICA DARK THEME ---
root = tk.Tk()
root.title("Cliente - Transmisor")
root.geometry("380x280")
root.configure(bg="#1E1E1E")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#1E1E1E", foreground="#D4D4D4", font=("Helvetica", 11, "bold"))
style.configure("TButton", background="#0E639C", foreground="white", font=("Helvetica", 11, "bold"), borderwidth=0)
style.map("TButton", background=[("active", "#1177BB")])

ttk.Label(root, text="Identidad del Remitente:").pack(anchor=tk.W, padx=20, pady=(20, 5))
entry_user = tk.Entry(root, font=("Helvetica", 12), bg="#3C3C3C", fg="white", insertbackground="white", relief="flat")
entry_user.pack(fill=tk.X, padx=20, ipady=6)

ttk.Label(root, text="Mensaje a Enviar:").pack(anchor=tk.W, padx=20, pady=(15, 5))
entry_text = tk.Entry(root, font=("Helvetica", 12), bg="#3C3C3C", fg="white", insertbackground="white", relief="flat")
entry_text.pack(fill=tk.X, padx=20, ipady=6)

btn_send = ttk.Button(root, text="Enviar al Servidor Central", command=send_message)
btn_send.pack(fill=tk.X, padx=20, pady=25, ipady=6)

root.mainloop()