import tkinter as tk
import requests

API_URL = "http://localhost:8080/api/clienteservidor/messages"

def refresh_messages():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            messages = response.json()
            
            # Borrar la lista actual y reescribirla con los datos nuevos
            listbox.delete(0, tk.END)
            for msg in messages:
                listbox.insert(tk.END, f"🟢 {msg['text']}")
    except:
        pass # Si falla, simplemente ignoramos y volvemos a intentar en el siguiente ciclo
        
    # Volver a ejecutar esta función dentro de 2000 milisegundos (2 segundos)
    root.after(2000, refresh_messages)

# Configuración de la Ventana del Servidor (Receptor)
root = tk.Tk()
root.title("ClienteServidor - Monitor del Servidor")
root.geometry("400x300")
root.configure(padx=20, pady=20)

tk.Label(root, text="Mensajes Recibidos:", font=("Arial", 14, "bold")).pack(pady=(0, 10))

# Lista donde aparecerán los mensajes
listbox = tk.Listbox(root, font=("Consolas", 12))
listbox.pack(fill=tk.BOTH, expand=True)

# Iniciar el ciclo de actualización automática
refresh_messages()

root.mainloop()