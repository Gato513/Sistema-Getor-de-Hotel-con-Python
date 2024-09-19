import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db.db_conection import habitaciones_de_empleados


class Avitacion_Empleados(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Habitacion de Empleados")

        #! Crear la tabla y definir las columnas en el frame derecho:
        self.tabla_habitacion_empleados = ttk.Treeview(self, columns=("id_estadia", "numero_habitacion", "tipo_habitacion", "costo", ), show="headings")

        #! Configurar las cabeceras de las columnas:
        self.tabla_habitacion_empleados.heading("id_estadia", text="Id")
        self.tabla_habitacion_empleados.heading("numero_habitacion", text="Habitacion de Empleados")
        self.tabla_habitacion_empleados.heading("tipo_habitacion", text="Tipo Habitacion")
        self.tabla_habitacion_empleados.heading("costo", text="Costo Habitacion")
        
        #! Layout de la tabla:
        self.tabla_habitacion_empleados.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

        self.cargar_info_Habitaciones()
        

    def cargar_info_Habitaciones(self):
        
        self.tabla_habitacion_empleados.delete(*self.tabla_habitacion_empleados.get_children())
        datos = habitaciones_de_empleados()

        for habitacion in datos:
            self.tabla_habitacion_empleados.insert("", "end", values=(
                habitacion.id_estadia,
                habitacion.numero_habitacion,
                habitacion.tipo_habitacion,
                habitacion.costo,
            )
        )