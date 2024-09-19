import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import os
from dotenv import load_dotenv
from main import MainApplication
from db.db_conection import start_connection, restart_session, close_session, User

from ventanas.modificar_contraseña import ModificarContraseña

#! Cargar variables de entorno desde el archivo .env
load_dotenv()

class LoginApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #! Inicializar conexión a la base de datos
        self.db_session = start_connection()

        #! Diseño de la GUI
        self.title("Sistema de Inicio de Sesión")
        self.geometry("400x300")

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        tk.Label(self, text="Usuario").grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")

        tk.Label(self, text="Contraseña").grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")

        self.login_button = tk.Button(self, text="Iniciar Sesión", command=self.attempt_login)
        self.login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")

    def verify_login(self, username, password):
        try:
            self.db_session = restart_session(self.db_session)
            user = self.db_session.query(User).filter_by(username=username).first()
            if not user:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")
                return False
            
            if user.is_first_time:
                messagebox.showinfo("Reseteo de Contraseña","Como ingresa por primera vez deve cambiar su contraseña por seguridad")
                self.load_modify_password_window(user.id)
                return False

            pepper = os.environ.get("PEPPER")
            if not pepper:
                raise ValueError("La variable de entorno PEPPER no está configurada")
            
            if bcrypt.checkpw(password.encode() + pepper.encode(), user.password.encode()):
                return user.role
            else: 
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar el inicio de sesión: {e}")
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")
            return False

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_role = self.verify_login(username, password)
        if user_role:
            messagebox.showinfo("Login", "¡Inicio de sesión exitoso!")
            close_session(self.db_session) #! Cerrar secion a la base de datos.
            self.destroy()
            self.load_main_window(user_role)

    def load_modify_password_window(self, id_usuario):
        ventana_referencia = ModificarContraseña(self, id_usuario, "user")
        ventana_referencia.transient(self)
        ventana_referencia.grab_set()
        self.wait_window(ventana_referencia)

    def load_main_window(self, user_role):
        main_window = MainApplication(user_role=user_role)
        main_window.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
