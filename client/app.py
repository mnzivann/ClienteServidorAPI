import tkinter as tk
from tkinter import messagebox
import requests

# URL actualizada con el nuevo nombre
API_URL = "http://localhost:8080/api/clienteservidor/messages"

def send_message():
    text = entry_message.get()
    if not text:
        return

    try:
        payload = {"text": text}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        entry_message.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Fallo de conexión:\n{e}")

root = tk.Tk()
root.title("ClienteServidor - Transmisor")
root.geometry("400x150")
root.configure(padx=20, pady=20)

tk.Label(root, text="Escribe un mensaje para el servidor:", font=("Arial", 12)).pack()
entry_message = tk.Entry(root, font=("Arial", 14), width=30)
entry_message.pack(pady=10)

tk.Button(root, text="Enviar Mensaje", command=send_message, bg="#0078D7", fg="white").pack()

root.mainloop()