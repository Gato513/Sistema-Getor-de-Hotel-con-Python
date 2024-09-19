import tkinter as tk
from tkinter import messagebox
import bcrypt
import os
from dotenv import load_dotenv
from db.db_conection import start_connection, close_session, User

load_dotenv()

class ModificarContraseña(tk.Toplevel):
    def __init__(self, parent, id_usuario, role):
        super().__init__(parent)
        self.parent = parent
        self.id_usuario = id_usuario
        self.role = role

        self.title("Modificar Contraseña")

        self.crear_widgets()

    def crear_widgets(self):
        #! Crear etiquetas
        tk.Label(self, text="Contraseña Nueva:").grid(row=0, column=0, padx=20, pady=20)
        tk.Label(self, text="Confirmar Contraseña:").grid(row=1, column=0, padx=20, pady=20)

        #! Crear entradas de contraseña
        self.entry_nueva_contraseña = tk.Entry(self, show="*")
        self.entry_nueva_contraseña.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        self.entry_confirmar_contraseña = tk.Entry(self, show="*")
        self.entry_confirmar_contraseña.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        #! Botón para guardar nueva contraseña
        self.boton_modificar_contraseña = tk.Button(self, text="Guardar", command=self.confirmar_datos_entrada)
        self.boton_modificar_contraseña.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def modificar_contraseña(self, password):
        try:
            #* Establecer la conexión a la base de datos
            session = start_connection()
            #! Obtener el usuario a modificar
            usuario_a_modificar = session.query(User).filter_by(id=self.id_usuario).first()
            
            if usuario_a_modificar is None:
                messagebox.showerror("Error", "Usuario no encontrado")
                return
            
            salt = bcrypt.gensalt()
            pepper = os.environ.get("PEPPER")
            if not pepper:
                raise ValueError("La variable de entorno PEPPER no está configurada")
            
            hashed_password = bcrypt.hashpw(password.encode() + pepper.encode(), salt)

            #! Actualizar la contraseña del usuario en la base de datos
            usuario_a_modificar.password = hashed_password.decode()
            usuario_a_modificar.salt = salt.decode()

            if self.role == "admin":
                usuario_a_modificar.is_first_time = True
            else: 
                usuario_a_modificar.is_first_time = False

            session.commit()

            #! Cerrar la conexión a la base de datos:
            close_session(session)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la contraseña: {e}")

    def confirmar_datos_entrada(self):
        nueva_contraseña = self.entry_nueva_contraseña.get()
        confirmar_contraseña = self.entry_confirmar_contraseña.get()

        if not nueva_contraseña or not confirmar_contraseña:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        if nueva_contraseña != confirmar_contraseña:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        self.modificar_contraseña(nueva_contraseña)
        messagebox.showinfo("Éxito", "¡Contraseña actualizada exitosamente!")

        self.destroy()
