import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db.db_conection import start_connection, close_session, User

from ventanas.modificar_contraseña import ModificarContraseña

class UserModify(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Modificar Usuarios")
        self.geometry("400x300")

        self.dibujar_tabla()
        self.dibujar_botones()
        self.cargar_usuarios()
        
    def dibujar_tabla(self):
        #! Configurar el grid para que la tabla ocupe todo el espacio:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #! Crear la tabla y definir las columnas:
        self.tabla_usuarios = ttk.Treeview(
            self, columns=("id", "nombre", "role"), show="headings"
        )

        #! Configurar las cabeceras de las columnas:
        columnas = ["id", "nombre", "role"]
        cabeceras = ["Id", "Numbre de Usuario", "Rol de Usuario"]

        for col, header in zip(columnas, cabeceras):
            self.tabla_usuarios.heading(col, text=header)

        #! Establecer ancho de columna:
        ancho_columna = 122
        for col in columnas:
            self.tabla_usuarios.column(col, width=ancho_columna, minwidth=ancho_columna, anchor=tk.CENTER)

        #! Layout de la tabla:
        self.tabla_usuarios.grid(row=0, column=0, sticky="nsew")

    def dibujar_botones(self):
        button_texts = ["Deshabilitar Usuario", "Modificar Contraseña"]
        commands = [self.disable_user, self.modify_password]

        for i, (text, command) in enumerate(zip(button_texts, commands)):
            button = tk.Button(self, text=text, command=command)
            button.grid(row=i + 1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

    def recuperar_id_usuario(self):
        seleccion = self.tabla_usuarios.focus()
        data_user = self.tabla_usuarios.item(seleccion, "values")
        return data_user[0]

    def cargar_usuarios(self):
        session = start_connection()
        usuarios = session.query(User).all()
        self.tabla_usuarios.delete(*self.tabla_usuarios.get_children())

        if not usuarios:
            print("Sin Datos")
            return

        for usuario in usuarios:
            self.tabla_usuarios.insert("", "end", values=(
                    usuario.id,
                    usuario.username,
                    usuario.role, 
                )
            )
        close_session(session)

    def disable_user(self):
        seleccion_user = self.tabla_usuarios.focus()
        id_usuario = self.recuperar_id_usuario()
        
        if not id_usuario:
            messagebox.showerror("Error", "Selecciones un usuario de la tabla")
            return
        
        session = start_connection()

        delete_user = session.query(User).filter_by(id=id_usuario).first()

        session.delete(delete_user)
        session.commit()
        close_session(session)

        self.tabla_usuarios.delete(seleccion_user)

    def load_modify_password_window(self, id_usuario):
        ventana_referencia = ModificarContraseña(self, id_usuario, "admin")
        ventana_referencia.transient(self)
        ventana_referencia.grab_set()
        self.wait_window(ventana_referencia)

    def modify_password(self):
        id_usuario = self.recuperar_id_usuario()
        
        if not id_usuario:
            messagebox.showerror("Error", "Selecciones un usuario de la tabla")
            return
        
        self.load_modify_password_window(id_usuario)
        self.cargar_usuarios()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  #! Oculta la ventana principal
    app = UserModify(root)
    app.mainloop()
