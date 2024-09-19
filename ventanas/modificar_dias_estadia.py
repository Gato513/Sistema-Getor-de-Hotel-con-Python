import tkinter as tk
from tkinter import ttk
from db.db_conection import start_connection


class ModificarDiasEstadia(tk.Toplevel):
    def __init__(self, parent, dias_anteriores):
        super().__init__(parent)
        self.parent = parent  # Guardar la referencia del padre
        self.dias_anteriores = dias_anteriores  # Guardar días de estadía anteriores

        self.title("Modificar Días de Estadia")

        # Establecer la conexión a la base de datos:
        self.session = start_connection()

        self.crear_widgets()

    def crear_widgets(self):
        # Crear etiqueta
        self.label_nueva_estadia = tk.Label(self, text="Nueva Estadia:")
        self.label_nueva_estadia.grid(row=0, column=0, padx=20, pady=20)

        # Crear entrada de días de estadia
        self.entry_nuevos_dias = tk.Entry(self)
        self.entry_nuevos_dias.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        self.entry_nuevos_dias.delete(0, tk.END)
        self.entry_nuevos_dias.insert(0, str(self.dias_anteriores))

        # Botón para modificar los días de estadia
        self.boton_modificar_dias = tk.Button(self, text="Modificar", command=self.modificar_dias_estadia)
        self.boton_modificar_dias.grid(row=1, column=0, padx=5, pady=5)

    def modificar_dias_estadia(self):
        # Recuperar el valor ingresado
        nuevos_dias = int(self.entry_nuevos_dias.get())

        # Enviar valor a modificar
        self.parent.modificar_dias_de_estadia(nuevos_dias)
        self.destroy()
