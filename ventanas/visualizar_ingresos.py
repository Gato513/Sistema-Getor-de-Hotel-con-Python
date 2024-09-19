from ctypes import pointer
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from db.db_conection import habitaciones_de_empleados, get_tipo_abitacion
class visualizar_ingresos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Visualizar los Ingresos")
        
        #! Crear un frame para contener la lista y la tabla
        self.frame_izquierdo = tk.Frame(self, bd=2)
        self.frame_izquierdo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.frame_derecho = tk.Frame(self, bd=2, relief="solid")
        self.frame_derecho.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.crear_frame_izquierdo()
        self.crear_frame_derecho()
        
    def crear_frame_izquierdo(self):
        #! Traer datos de tipo de abitacion disponible:
        tipos_de_abitaciones = get_tipo_abitacion()

        #! Crear lista desplegable y asignar la opcion inicial
        self.lista_dias = ttk.Combobox(self.frame_izquierdo, values = tipos_de_abitaciones)
        self.lista_dias.grid(row=0, column=0, padx=5, pady=5, sticky="ew", ipady=5)
        self.lista_dias.current(0)

        #! Configurar distribucion de espacion entre filas:
        numero_row = 2
        for i in range(numero_row):
            self.frame_izquierdo.grid_rowconfigure(i, weight=5)

        #! Boton para traer los totales de ingresos:
        self.boton_calcular = tk.Button(self.frame_izquierdo, text="Calcular", command=self.cargar_info_Habitaciones, bg="blue", fg="white", cursor="hand2")
        self.boton_calcular.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        
    def crear_frame_derecho(self):
        #! Configurar el grid para que la tabla ocupe todo el espacio:
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)

        #! Crear la tabla y definir las columnas en el frame derecho:
        self.tabla_ingresos = ttk.Treeview(
            self.frame_derecho, columns=("tipo", "dias", "recaudacion_total"), show="headings"
        )

        #! Configurar las cabeceras de las columnas:
        columnas = ["tipo", "dias", "recaudacion_total"]
        cabeceras = ["Tipo", "Dias de Estadias", " Recaudacion Total"]

        for col, header in zip(columnas, cabeceras):
            self.tabla_ingresos.heading(col, text=header)

        #! Establecer ancho de columna:
        ancho_columna = 122
        for col in columnas:
            self.tabla_ingresos.column(col, width=ancho_columna, minwidth=ancho_columna, anchor=tk.CENTER)

        #! Layout de la tabla:
        self.tabla_ingresos.grid(row=0, column=0, sticky="nsew")
                
    def cargar_info_Habitaciones(self):
        tipo_habitacion = self.lista_dias.get()
        self.tabla_ingresos.delete(*self.tabla_ingresos.get_children())
        total = habitaciones_de_empleados(tipo_habitacion)
        self.tabla_ingresos.insert("", "end", values=(tipo_habitacion, total[0], total[1]))


