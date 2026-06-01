import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_MESSAGES = "http://localhost:8081/api/clienteservidor/messages"
API_USERS = "http://localhost:8081/api/clienteservidor/users"

class ReceptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Receptor - Panel de Administración CRUD")
        self.root.geometry("850x550")
        self.root.configure(bg="#1E1E1E") # Fondo oscuro principal
        
        self.selected_msg_id = None
        self.is_editing = False # Controla la pausa de actualizaciones

        # --- CONFIGURACIÓN DE ESTILOS (DARK THEME) ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1E1E1E")
        style.configure("TLabel", background="#1E1E1E", foreground="#D4D4D4", font=("Helvetica", 11, "bold"))
        style.configure("TButton", background="#0E639C", foreground="white", borderwidth=0, font=("Helvetica", 10))
        style.map("TButton", background=[("active", "#1177BB")], foreground=[("disabled", "#808080")])
        
        # Estilos específicos de la tabla (Treeview)
        style.configure("Treeview", background="#2D2D2D", foreground="#D4D4D4", fieldbackground="#2D2D2D", borderwidth=0, font=("Helvetica", 11))
        style.configure("Treeview.Heading", background="#252526", foreground="white", font=("Helvetica", 11, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", "#094771")])

        # --- PANEL SUPERIOR: EDICIÓN ---
        frame_edit = ttk.Frame(self.root)
        frame_edit.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(frame_edit, text="Editar Mensaje:").pack(side=tk.LEFT, padx=5)
        
        # Caja de texto estilizada
        self.entry_edit = tk.Entry(frame_edit, font=("Helvetica", 12), bg="#3C3C3C", fg="white", insertbackground="white", state="disabled", relief="flat")
        self.entry_edit.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=5)

        self.btn_save = ttk.Button(frame_edit, text="Guardar", command=self.save_edit, state="disabled")
        self.btn_save.pack(side=tk.LEFT, padx=5, ipady=4)
        
        self.btn_cancel = ttk.Button(frame_edit, text="Cancelar Acción", command=self.cancel_action, state="disabled")
        self.btn_cancel.pack(side=tk.LEFT, padx=5, ipady=4)

        # --- PANEL INFERIOR: TABLAS DE DATOS ---
        frame_data = ttk.Frame(self.root)
        frame_data.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Columna Izquierda: Tabla de Mensajes
        frame_msg = ttk.Frame(frame_data)
        frame_msg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        ttk.Label(frame_msg, text="Buzón de Mensajes").pack(anchor=tk.W, pady=(0, 8))
        self.tree = ttk.Treeview(frame_msg, columns=("id", "usuario", "mensaje"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("mensaje", text="Texto del Mensaje")
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("usuario", width=120)
        self.tree.column("mensaje", width=300)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_select_message)

        ttk.Button(frame_msg, text="Eliminar Mensaje Seleccionado", command=self.delete_message).pack(pady=10, fill=tk.X, ipady=3)

        # Columna Derecha: Lista de Usuarios
        frame_usr = ttk.Frame(frame_data)
        frame_usr.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Label(frame_usr, text="Usuarios Registrados").pack(anchor=tk.W, pady=(0, 8))
        
        # Lista de usuarios estilizada
        self.list_usr = tk.Listbox(frame_usr, font=("Helvetica", 11), bg="#2D2D2D", fg="#D4D4D4", selectbackground="#094771", selectborderwidth=0, relief="flat", highlightthickness=0, width=25)
        self.list_usr.pack(fill=tk.BOTH, expand=True)
        
        # EL FIX: Al tocar un usuario, se pausa la actualización
        self.list_usr.bind("<<ListboxSelect>>", self.on_select_user) 

        ttk.Button(frame_usr, text="Eliminar Usuario", command=self.delete_user).pack(pady=10, fill=tk.X, ipady=3)

        self.refresh_data()

    # --- LÓGICA CRUD ---
    def refresh_data(self):
        # Solo actualiza si NO estamos seleccionando/editando nada
        if not self.is_editing:
            try:
                res_msg = requests.get(API_MESSAGES)
                if res_msg.status_code == 200:
                    for row in self.tree.get_children():
                        self.tree.delete(row)
                    for m in res_msg.json():
                        self.tree.insert("", tk.END, values=(m['id'], m['sender'], m['text']))
                
                res_usr = requests.get(API_USERS)
                if res_usr.status_code == 200:
                    self.list_usr.delete(0, tk.END)
                    for u in res_usr.json():
                        self.list_usr.insert(tk.END, u)
            except:
                pass
                
        self.root.after(500, self.refresh_data)

    def on_select_message(self, event):
        selected = self.tree.focus()
        if selected:
            self.is_editing = True # Pausa la tabla
            valores = self.tree.item(selected, 'values')
            self.selected_msg_id = valores[0]
            
            self.entry_edit.config(state="normal")
            self.entry_edit.delete(0, tk.END)
            self.entry_edit.insert(0, valores[2])
            
            self.btn_save.config(state="normal")
            self.btn_cancel.config(state="normal")
            self.list_usr.selection_clear(0, tk.END) # Quita selección de usuarios

    def on_select_user(self, event):
        if self.list_usr.curselection():
            self.is_editing = True # Pausa la tabla para que no se borre tu selección
            self.btn_cancel.config(state="normal") # Habilita botón para cancelar acción

    def save_edit(self):
        nuevo_texto = self.entry_edit.get().strip()
        if self.selected_msg_id and nuevo_texto:
            requests.put(API_MESSAGES, json={"id": self.selected_msg_id, "text": nuevo_texto})
            self.cancel_action()

    def cancel_action(self):
        # Limpia todo y reanuda el ciclo de actualización
        self.is_editing = False
        self.selected_msg_id = None
        self.entry_edit.delete(0, tk.END)
        self.entry_edit.config(state="disabled")
        self.btn_save.config(state="disabled")
        self.btn_cancel.config(state="disabled")
        self.list_usr.selection_clear(0, tk.END)

    def delete_message(self):
        selected = self.tree.focus()
        if selected:
            msg_id = self.tree.item(selected, 'values')[0]
            requests.delete(f"{API_MESSAGES}?id={msg_id}")
            self.cancel_action()

    def delete_user(self):
        seleccion = self.list_usr.curselection()
        if seleccion:
            nombre = self.list_usr.get(seleccion[0])
            if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar a '{nombre}'?\nEsto borrará todos sus mensajes del servidor."):
                requests.delete(f"{API_USERS}?name={nombre}")
            self.cancel_action()
        else:
            messagebox.showwarning("Atención", "Por favor, haz clic en un usuario de la lista primero.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceptorApp(root)
    root.mainloop()