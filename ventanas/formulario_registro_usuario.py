import tkinter as tk
from tkinter import messagebox
import bcrypt
import os
from dotenv import load_dotenv
from db.db_conection import start_connection, User

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class formulario_registro_usuario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        #! Inicializar conexión a la base de datos
        self.session = start_connection()

        #! Diseño de la GUI
        self.title("Registro de Usuarios")
        self.geometry("400x350")  #! Aumentar el tamaño de la ventana para acomodar los widgets más grandes

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        tk.Label(self, text="Usuario").grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura de la entrada

        tk.Label(self, text="Contraseña").grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura de la entrada

        tk.Label(self, text="Confirmar Contraseña").grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")

        self.login_button = tk.Button(self, text="Registrar", command=self.register)
        self.login_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura del botón

    def create_user(self, username, password):
        try:
            salt = bcrypt.gensalt()
            pepper = os.environ.get("PEPPER")
            if not pepper:
                raise ValueError("La variable de entorno PEPPER no está configurada")
            hashed_password = bcrypt.hashpw(password.encode() + pepper.encode(), salt)
            new_user = User(
                username=username, 
                password=hashed_password.decode(), 
                salt=salt.decode()
            )
            self.session.add(new_user)
            self.session.commit()
            messagebox.showinfo("Registro", "¡Usuario creado exitosamente!")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el usuario: {e}")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username and not password and not confirm_password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        if  password != confirm_password:
            messagebox.showerror("Error", "La contraseña no coincide con la confirmacion")
            return

        self.create_user(username, password)

        #! Limpiar entradas de datos:
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)