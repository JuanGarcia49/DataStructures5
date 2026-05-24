import tkinter as tk

from tkinter import messagebox
from tkinter import ttk # Importar ttk para el Combobox
from tkcalendar import DateEntry
from tkinter import simpledialog # Para pedir el ID al eliminar de la lista
from datetime import date

# --- Clases para la gestión de estructuras de datos ---
class EstructuraDatos:
    """Clase madre para gestionar registros en diferentes estructuras de datos."""
    def __init__(self):
        self.data = []

    def agregar(self, item):
        """Metodo para agregar un elemento a la estructura de datos."""
        raise NotImplementedError("El metodo 'agregar' debe ser implementado por las subclases.")
    
    def eliminar(self, id_number=None):
        """Metodo para eliminar un elemento de la estructura de datos."""
        raise NotImplementedError("El metodo 'eliminar' debe ser implementado por las subclases.")

    def obtener_todos(self):
        """Retorna todos los elementos de la estructura."""
        return self.data

    def __str__(self):
        return f"{self.__class__.__name__}: {self.data}"

class Pila(EstructuraDatos):
    """Clase para gestionar registros como una Pila (LIFO)."""
    def __init__(self):
        super().__init__()
        self.nombre = "Pila"

    def agregar(self, item):
        self.data.append(item)

    def eliminar(self, id_number=None): # id_number es ignorado para Pila
        if not self.data:
            return None
        return self.data.pop() # Elimina el ultimo (LIFO)

class Cola(EstructuraDatos):
    """Clase para gestionar registros como una Cola (FIFO)."""
    def __init__(self):
        super().__init__()
        self.nombre = "Cola"

    def agregar(self, item):
        self.data.append(item)
    
    def eliminar(self, id_number=None): # id_number es ignorado para Cola
        if not self.data:
            return None
        return self.data.pop(0) # Elimina el primero (FIFO)

class Lista(EstructuraDatos):
    """Clase para gestionar registros como una Lista."""
    def __init__(self):
        super().__init__()
        self.nombre = "Lista"

    def agregar(self, item):
        self.data.append(item)
    
    def eliminar(self, id_number):
        if not id_number:
            return False
        for i, afiliado in enumerate(self.data):
            if afiliado.get("numero_identificacion") == id_number:
                del self.data[i]
                return True
        return False # No encontrado


def abrir_control_afiliados():
    registro = tk.Tk()
    registro.title("Caja Compensandote - Control de Afiliados")
    registro.geometry("1300x650")
    registro.resizable(False, False)

    # --- Instancias de las estructuras de datos ---
    estructuras_disponibles = {
        "Pila": Pila(),
        "Cola": Cola(),
        "Lista": Lista()
    }

    def tarifa_ingreso_empleado(ingreso):
        #Calcula la tarifa de afiliacion basada en el ingreso mensual.
        tarifa = 0
        if 1000000 <= ingreso <= 2000000:
            tarifa = 45000
        elif 2000001 <= ingreso <= 3000000:
            tarifa = 60000
        elif 3000001 <= ingreso <= 4000000:
            tarifa = 75000
        elif 4000001 <= ingreso <= 5000000:
            tarifa = 90000
        elif ingreso > 5000000:
            tarifa = 150000
        return tarifa
    
    def tarifa_ingreso_independiente(ingreso):
        #Calcula la tarifa de afiliación basada en el ingreso mensual.
        tarifa = 0
        if 1000000 <= ingreso <= 2000000:
            tarifa = 10000
        elif 2000001 <= ingreso <= 3000000:
            tarifa = 20000
        elif 3000001 <= ingreso <= 4000000:
            tarifa = 30000
        elif 4000001 <= ingreso <= 5000000:
            tarifa = 40000
        elif ingreso > 5000000:
            tarifa = 80000
        return tarifa
    
    def tarifa_extra(servicio, ingreso):
        #Calcula la tarifa de afiliación basada en el ingreso mensual.
        tarifa = 0
        if servicio == "Subsidio de desempleo":
            tarifa = 0
        elif servicio == "Ingreso a parque":
            tarifa = 2500
        elif servicio == "Curso de formacion":
            tarifa = 7500
        elif servicio == "Paquete de viaje":
            tarifa = 10000
        elif servicio == "Medicina preventiva":
            tarifa = ingreso * 0.10 # 10% del ingreso
        return tarifa

    # --- Funciones de Validación ---
    def validar_solo_numeros(P):
        return P == "" or P.isdigit()
    vcmd_num = (registro.register(validar_solo_numeros), '%P')

    def validar_solo_letras(P):
        return all(c.isalpha() or c.isspace() for c in P)
    vcmd_alpha = (registro.register(validar_solo_letras), '%P')

    # --- Variable de control para el formateo de ingresos ---
    # Bandera para evitar recursion infinita en el trace_add
    ingresos_actuales_var = tk.StringVar()
    _formatting_active = False

    def format_ingresos_input(*args):
        nonlocal _formatting_active
        if _formatting_active:
            return
        
        _formatting_active = True
        try:
            current_value = ingresos_actuales_var.get()
            # Limpiar el valor, dejando solo dígitos
            cleaned_value = ''.join(filter(str.isdigit, current_value))

            if not cleaned_value:
                ingresos_actuales_var.set("")
            else:
                num = int(cleaned_value)
                formatted_num = "{:,.0f}".format(num) # Formato con separador de miles
                ingresos_actuales_var.set(formatted_num)
        finally:
            _formatting_active = False

    # --- Variables de Control de Tkinter para los campos del formulario ---
    # --- Datos para el Formulario ---
    documentos_identidad = ["CC", "CE", "NUIP", "PAS"]
    servicios = [
        "Subsidio de desempleo",
        "Ingreso a parque",
        "Curso de formacion",
        "Paquete de viaje",
        "Medicina preventiva"
        ]
    
    # Variables para los widgets
    estructura_seleccionada_var = tk.StringVar(value="Pila") # Valor por defecto
    tipo_identificacion_var = tk.StringVar(value=documentos_identidad[0]) # Valor por defecto
    numero_identificacion_var = tk.StringVar()
    nombre_completo_var = tk.StringVar()
    modalidad_empleo_var = tk.StringVar(value="Empleado") # Valor por defecto
    servicio_deseado_var = tk.StringVar(value=servicios[0]) # Valor por defecto
    resultado_var = tk.StringVar() # Para la tarifa total

    # --- Funcion para actualizar la vista del TreeView ---
    def actualizar_vista_treeview(event=None):
        # Obtener la estructura seleccionada para la vista
        vista_seleccionada = combo_vista_estructura.get()
        estructura = estructuras_disponibles.get(vista_seleccionada)

        # Limpiar el TreeView
        for item in tree.get_children():
            tree.delete(item)

        if estructura:
            # Poblar el TreeView con los datos de la estructura
            for i, afiliado in enumerate(estructura.obtener_todos()):
                tree.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        afiliado.get("numero_identificacion", ""),
                        afiliado.get("nombre_completo", ""),
                        f"${afiliado.get('ingresos_actuales', 0):,.0f}",
                        f"${afiliado.get('tarifa_afiliacion', 0):,.0f}",
                        afiliado.get("fecha_afiliacion", ""),
                        afiliado.get("servicio_deseado", "")
                    )
                )

    # --- Funcion Principal de Calculo ---
    def calcular_tarifa_final():
        try:
            # Limpiar el string de ingresos antes de convertir a float
            ingreso_str = ''.join(filter(str.isdigit, ingresos_actuales_var.get()))
            modalidad = modalidad_empleo_var.get()
            servicio = servicio_deseado_var.get()

            # 2. Validar que los campos necesarios para el calculo no esten vacios
            if not all([ingreso_str, modalidad, servicio]):
                messagebox.showwarning("Campos Incompletos", "Por favor, complete los campos de Ingresos, Modalidad y Servicio para el calculo.", parent=registro)
                return

            ingreso = float(ingreso_str)
            tarifa_base = 0

            # 3. Calcular tarifa base segun la modalidad
            if modalidad == "Empleado":
                tarifa_base = tarifa_ingreso_empleado(ingreso)
            elif modalidad == "Independiente":
                tarifa_base = tarifa_ingreso_independiente(ingreso)

            # 4. Calcular tarifa extra según el servicio
            t_extra = tarifa_extra(servicio, ingreso)

            # 5. Calcular total y actualizar la etiqueta de resultado
            total = tarifa_base + t_extra
            resultado_var.set(f"${total:,.0f}")

        except ValueError:
            messagebox.showerror("Error de Datos", "El campo 'Ingresos Actuales' debe ser un número válido.", parent=registro)

    # --- Funcion para registrar afiliado ---
    def registrar_afiliado():
        try:
            # 1. Intentar calcular la tarifa primero. La funcion de calculo mostrara sus propios errores si es necesario.
            calcular_tarifa_final()
            tarifa_total_str = resultado_var.get()

            # 2. Si despues del calculo, la tarifa sigue vacía, la funcion de calculo ya mostro un error - salimos.
            if not tarifa_total_str:
                return

            # 3. Recopilar el resto de los datos del formulario
            tipo_estructura = estructura_seleccionada_var.get()
            tipo_id = tipo_identificacion_var.get()
            num_id = numero_identificacion_var.get()
            nombre = nombre_completo_var.get()
            ingreso_str_raw = ingresos_actuales_var.get() # Valor formateado del campo
            ingreso_str_cleaned = ''.join(filter(str.isdigit, ingreso_str_raw)) # Limpio para calculo
            fecha_afiliacion = widgets["fecha_afiliacion"].get_date().strftime("%d/%m/%Y")
            modalidad = modalidad_empleo_var.get()
            servicio = servicio_deseado_var.get()

            # 4. Validar que todos los campos (incluyendo los que no son para el calculo) esten diligenciados
            if not all([tipo_estructura, tipo_id, num_id, nombre, ingreso_str_cleaned, fecha_afiliacion, modalidad, servicio]):
                messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos antes de registrar.", parent=registro)
                return

            # Convertir ingreso y tarifa_total a tipos apropiados
            ingreso = float(ingreso_str_cleaned)
            # Eliminar '$' y ',' de tarifa_total_str antes de convertir a float
            tarifa_total = float(tarifa_total_str.replace('$', '').replace(',', ''))

            # Crear un diccionario con los datos del afiliado
            afiliado_data = {
                "tipo_identificacion": tipo_id,
                "numero_identificacion": num_id,
                "nombre_completo": nombre,
                "ingresos_actuales": ingreso,
                "fecha_afiliacion": fecha_afiliacion,
                "modalidad_empleo": modalidad,
                "servicio_deseado": servicio,
                "tarifa_afiliacion": tarifa_total
            }

            # 3. Obtener la instancia de la estructura de datos seleccionada
            estructura = estructuras_disponibles.get(tipo_estructura)

            if estructura:
                estructura.agregar(afiliado_data)
                messagebox.showinfo("Registro Exitoso", f"Afiliado '{nombre}' registrado en la {tipo_estructura}.", parent=registro)
                
                # Actualizar el TreeView si se esta mostrando la estructura modificada
                if tipo_estructura == combo_vista_estructura.get():
                    actualizar_vista_treeview()
                
                limpiar_formulario()
            else:
                messagebox.showerror("Error", "Tipo de estructura de datos no válido.", parent=registro)

        except ValueError:
            messagebox.showerror("Error de Datos", "Asegurese de que 'Ingresos Actuales' y 'Tarifa Total' sean numeros validos.", parent=registro)
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrio un error al registrar: {e}", parent=registro)

    # --- Funcion para limpiar el formulario ---
    def limpiar_formulario():
        tipo_identificacion_var.set(documentos_identidad[0]) # Reset a valor por defecto
        numero_identificacion_var.set("")
        nombre_completo_var.set("")
        ingresos_actuales_var.set("") # Limpia el campo formateado
        widgets["fecha_afiliacion"].set_date(date.today())
        modalidad_empleo_var.set("Empleado") # Reset a valor por defecto
        servicio_deseado_var.set(servicios[0]) # Reset a valor por defecto
        resultado_var.set("") # Limpia el campo de tarifa

    # --- Funcion para generar el reporte de la estructura seleccionada ---
    def generar_reporte():
        try:
            # 1. Obtener la estructura seleccionada para la vista
            vista_seleccionada = combo_vista_estructura.get()
            estructura = estructuras_disponibles.get(vista_seleccionada)

            if not estructura or not estructura.obtener_todos():
                messagebox.showinfo("Reporte Vacío", f"No hay registros en la {vista_seleccionada} para generar un reporte.", parent=registro)
                return

            # 2. Calcular la suma de las tarifas
            total_tarifas = sum(afiliado.get('tarifa_afiliacion', 0) for afiliado in estructura.obtener_todos())
            numero_registros = len(estructura.obtener_todos())

            # 3. Crear el mensaje del reporte
            mensaje_reporte = (
                f"--- Reporte de la {vista_seleccionada} ---\n\n"
                f"Numero de registros: {numero_registros}\n"
                f"Suma total de tarifas de afiliacion: ${total_tarifas:,.0f}"
            )
            messagebox.showinfo(f"Reporte - {vista_seleccionada}", mensaje_reporte, parent=registro)
        except Exception as e:
            messagebox.showerror("Error en Reporte", f"Ocurrió un error al generar el reporte: {e}", parent=registro)

    # --- Funcion para eliminar afiliado de la estructura seleccionada ---
    def eliminar_afiliado_seleccionado():
        vista_seleccionada = combo_vista_estructura.get()
        estructura = estructuras_disponibles.get(vista_seleccionada)

        if not estructura or not estructura.obtener_todos():
            messagebox.showinfo("Eliminar", f"No hay registros en la {vista_seleccionada} para eliminar.", parent=registro)
            return

        if not messagebox.askyesno("Confirmar Eliminacion", f"Esta seguro que desea eliminar un registro de la {vista_seleccionada}?", parent=registro):
            return

        if vista_seleccionada == "Lista":
            id_a_eliminar = simpledialog.askstring("Eliminar de Lista", "Ingrese el número de identificación del afiliado a eliminar:", parent=registro)
            if not id_a_eliminar:
                messagebox.showwarning("Eliminar", "Debe ingresar un numero de identificación para eliminar de la Lista.", parent=registro)
                return
            
            if estructura.eliminar(id_a_eliminar):
                messagebox.showinfo("Eliminar", f"Afiliado con ID {id_a_eliminar} eliminado de la Lista.", parent=registro)
            else:
                messagebox.showwarning("Eliminar", f"Afiliado con ID {id_a_eliminar} no encontrado en la Lista.", parent=registro)
        else: # Pila o Cola
            afiliado_eliminado = estructura.eliminar()
            if afiliado_eliminado:
                messagebox.showinfo(
                    "Eliminar", 
                    f"Registro eliminado de la {vista_seleccionada}:\n"
                    f"ID: {afiliado_eliminado.get('numero_identificacion', 'N/A')}\n"
                    f"Nombre: {afiliado_eliminado.get('nombre_completo', 'N/A')}", 
                    parent=registro
                )
            else:
                messagebox.showerror("Error", f"No se pudo eliminar de la {vista_seleccionada}.", parent=registro)
        
        actualizar_vista_treeview() # Refrescar la vista después de la eliminación

    # --- Configuracion de la Interfaz Gráfica (UI) ---
    registro.grid_columnconfigure(0, weight=2) # 40%
    registro.grid_columnconfigure(1, weight=3) # 60%
    registro.grid_rowconfigure(0, weight=1)

    # --- Sidebar (Formulario) ---
    frame_sidebar = tk.Frame(registro, bd=2, relief="sunken", padx=15, pady=15)
    frame_sidebar.grid(row=0, column=0, sticky="nsew")
    frame_sidebar.columnconfigure(1, weight=1)

    widgets = {}
    labels_texto = ["Estructura de Datos:", "Tipo de Identificación:", "Número de Identificación:", "Nombre Completo:", "Ingresos Actuales:", "Fecha de Afiliación:", "Modalidad de Empleo:", "Servicio Deseado:"]

    for i, texto in enumerate(labels_texto):
        tk.Label(frame_sidebar, text=texto, font=("Helvetica", 12)).grid(row=i, column=0, padx=5, pady=8, sticky="w")

    # --- Creación de Widgets del Formulario ---
    widgets["estructura_datos"] = ttk.Combobox(frame_sidebar, textvariable=estructura_seleccionada_var, values=list(estructuras_disponibles.keys()), font=("Helvetica", 12), state="readonly")
    widgets["tipo_identificacion"] = ttk.Combobox(frame_sidebar, textvariable=tipo_identificacion_var, values=documentos_identidad, font=("Helvetica", 12), state="readonly")
    widgets["numero_identificacion"] = tk.Entry(frame_sidebar, textvariable=numero_identificacion_var, font=("Helvetica", 12), validate="key", validatecommand=vcmd_num)
    widgets["nombre_completo"] = tk.Entry(frame_sidebar, textvariable=nombre_completo_var, font=("Helvetica", 12), validate="key", validatecommand=vcmd_alpha)
    widgets["ingresos_actuales"] = tk.Entry(frame_sidebar, textvariable=ingresos_actuales_var, font=("Helvetica", 12)) # Ya no usa vcmd_num
    widgets["fecha_afiliacion"] = DateEntry(frame_sidebar, font=("Helvetica", 12), date_pattern='dd/mm/yyyy', width=12, background='darkblue', foreground='white', borderwidth=2)

    frame_modalidad = tk.Frame(frame_sidebar)
    tk.Radiobutton(frame_modalidad, text="Empleado", variable=modalidad_empleo_var, value="Empleado", font=("Helvetica", 11)).pack(side="left")
    tk.Radiobutton(frame_modalidad, text="Independiente", variable=modalidad_empleo_var, value="Independiente", font=("Helvetica", 11)).pack(side="left", padx=10)

    # --- Posicionamiento de Widgets en la Rejilla ---
    widgets["estructura_datos"].grid(row=0, column=1, padx=5, pady=8, sticky="ew")
    widgets["tipo_identificacion"].grid(row=1, column=1, padx=5, pady=8, sticky="ew")
    widgets["numero_identificacion"].grid(row=2, column=1, padx=5, pady=8, sticky="ew")
    widgets["nombre_completo"].grid(row=3, column=1, padx=5, pady=8, sticky="ew")
    widgets["ingresos_actuales"].grid(row=4, column=1, padx=5, pady=8, sticky="ew")
    widgets["fecha_afiliacion"].grid(row=5, column=1, padx=5, pady=8, sticky="ew")
    frame_modalidad.grid(row=6, column=1, padx=5, pady=8, sticky="w")
    widgets["servicio_deseado"] = ttk.Combobox(frame_sidebar, textvariable=servicio_deseado_var, values=servicios, font=("Helvetica", 12), state="readonly")
    widgets["servicio_deseado"].grid(row=7, column=1, padx=5, pady=8, sticky="ew")

    # --- Boton de Acción ---
    tk.Button(frame_sidebar, text="Calcular Tarifa de Afiliación", command=calcular_tarifa_final, font=("Helvetica", 12, "bold")).grid(row=8, column=0, columnspan=2, pady=10)

    # --- Campo de Tarifa Total (no editable) ---
    tk.Label(frame_sidebar, text="Tarifa Total de Afiliación:", font=("Helvetica", 12)).grid(row=9, column=0, padx=5, pady=8, sticky="w")
    entry_tarifa_total = tk.Entry(frame_sidebar, textvariable=resultado_var, font=("Helvetica", 12, "bold"), state="readonly", fg="blue")
    entry_tarifa_total.grid(row=9, column=1, padx=5, pady=8, sticky="ew")

    # --- Botones de Registro y Limpieza ---
    frame_botones_accion = tk.Frame(frame_sidebar)
    frame_botones_accion.grid(row=10, column=0, columnspan=2, pady=20)
    tk.Button(frame_botones_accion, text="Registrar Afiliado", command=registrar_afiliado, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones_accion, text="Limpiar Formulario", command=limpiar_formulario, font=("Helvetica", 12)).pack(side="left", padx=5) # Columna 1
    tk.Button(frame_botones_accion, text="Salir", command=registro.destroy, font=("Helvetica", 12)).pack(side="left", padx=5) # Columna 2

    # --- Main Content (Visualizacion de Datos) ---
    frame_main_content = tk.Frame(registro, padx=15, pady=15)
    frame_main_content.grid(row=0, column=1, sticky="nsew")
    frame_main_content.grid_rowconfigure(2, weight=1) # Fila del TreeView se expande
    frame_main_content.grid_columnconfigure(0, weight=1) # Columna del TreeView se expande

    # Dropdown para seleccionar la vista de la estructura
    tk.Label(frame_main_content, text="Mostrar datos de:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    # --- Contenedor para la selección de vista y reporte ---
    frame_vista_controles = tk.Frame(frame_main_content)
    frame_vista_controles.grid(row=1, column=0, sticky="ew", pady=(0, 15))
    frame_vista_controles.columnconfigure(0, weight=1) # El combobox se expande

    combo_vista_estructura = ttk.Combobox(frame_vista_controles, values=list(estructuras_disponibles.keys()), font=("Helvetica", 12), state="readonly")
    combo_vista_estructura.grid(row=0, column=0, sticky="ew")
    combo_vista_estructura.bind("<<ComboboxSelected>>", actualizar_vista_treeview)

    # Boton de Eliminar
    tk.Button(frame_vista_controles, text="Eliminar", command=eliminar_afiliado_seleccionado, font=("Helvetica", 12)).grid(row=0, column=2, padx=(10, 0))

    # Boton de Reporte
    tk.Button(frame_vista_controles, text="Reporte", command=generar_reporte, font=("Helvetica", 12)).grid(row=0, column=1, padx=(10, 0))

    # TreeView para mostrar los datos
    tree_frame = tk.Frame(frame_main_content)
    tree_frame.grid(row=2, column=0, sticky="nsew")
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    tree_scrollbar = tk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, selectmode="extended")
    tree.pack(side="left", fill="both", expand=True)
    tree_scrollbar.config(command=tree.yview)

    # Definir columnas del TreeView
    tree["columns"] = ("ID", "Nombre", "Ingresos", "Tarifa", "Fecha", "Servicio")
    tree.column("#0", width=0, stretch=tk.NO) # Columna fantasma
    tree.column("ID", anchor=tk.W, width=120)
    tree.column("Nombre", anchor=tk.W, width=200)
    tree.column("Ingresos", anchor=tk.E, width=120)
    tree.column("Tarifa", anchor=tk.E, width=120)
    tree.column("Fecha", anchor=tk.CENTER, width=100)
    tree.column("Servicio", anchor=tk.W, width=150)

    # Crear encabezados
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("ID", text="Identificación", anchor=tk.W)
    tree.heading("Nombre", text="Nombre Completo", anchor=tk.W)
    tree.heading("Ingresos", text="Ingresos", anchor=tk.E)
    tree.heading("Tarifa", text="Tarifa Afiliación", anchor=tk.E)
    tree.heading("Fecha", text="Fecha Afiliación", anchor=tk.CENTER)
    tree.heading("Servicio", text="Servicio Deseado", anchor=tk.W)

    # Enlazar la funcion de formato al campo de ingresos
    ingresos_actuales_var.trace_add("write", format_ingresos_input)

    # Establecer valores iniciales para los Comboboxes y Radiobuttons
    widgets["tipo_identificacion"].set(documentos_identidad[0])
    widgets["servicio_deseado"].set(servicios[0])
    widgets["estructura_datos"].set(list(estructuras_disponibles.keys())[0])
    combo_vista_estructura.set(list(estructuras_disponibles.keys())[0]) # Valor por defecto para el TreeView

    # Llamar a la funcion una vez para poblar la vista inicial
    actualizar_vista_treeview()


def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculacion con eventos de teclado.
    """
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "Caja":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Cierra la ventana de login
        abrir_control_afiliados()
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            messagebox.showwarning("Acceso Denegado", f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END) # Limpia el campo de contraseña
        else:
            messagebox.showerror("Acceso Bloqueado", "Ha superado el número de intentos permitidos.", parent=ventana)
            ventana.destroy() # Cierra la aplicación

def acerca_de(event=None):
    titulo = "Acerca de"
    mensaje = (
        "Programa: Estructura de datos\n"
        "Estudiante: Juan Pablo Garcia\n"
        "Numero de grupo colaborativo: 301305A_2201"
    )
    messagebox.showinfo(titulo, mensaje, parent=ventana)


# --- Configuración de la Ventana Principal (Login) ---
ventana = tk.Tk()
ventana.title("Login - Compensandote")
ventana.geometry("540x220") # Aumentamos la altura para asegurar que los botones sean visibles
ventana.resizable(False, False)

# --- Barra superior con el boton "Acerca de" ---
# En lugar de un menú (que en macOS se va a la barra superior de la pantalla),
# creamos un Frame para simular una barra dentro de la ventana.
frame_menu = tk.Frame(ventana, relief="raised", bd=1)
frame_menu.pack(side="top", fill="x")
# Añadimos un botón con apariencia plana (flat) para que parezca un texto de menú.
tk.Button(frame_menu, text="Acerca de...", command=acerca_de, relief="flat").pack(side="left")

# --- Creación de Widgets ---
tk.Label(ventana, text="Ingrese la contraseña de acceso:").pack(pady=10)

# Este es el campo de entrada para la contraseña. La opción show="*" oculta el texto.
entry_contrasena = tk.Entry(ventana, show="*", font=("Helvetica", 12), width=25)
entry_contrasena.pack(pady=5)
# Vinculamos la tecla "Enter" (Return) al campo de contraseña para llamar a la función de verificación.
entry_contrasena.bind('<Return>', verificar_contrasena)

label_intentos = tk.Label(ventana, text="Intentos restantes: 3")
label_intentos.pack(pady=5)

# --- Contenedor para los botones ---
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Ingresar", command=verificar_contrasena, font=("Helvetica", 12)).grid(row=0, column=0, padx=10) # Columna 0
tk.Button(frame_botones, text="Salir", command=ventana.destroy, font=("Helvetica", 12)).grid(row=0, column=1, padx=10) # Columna 1

# Iniciar el bucle de eventos para que la ventana aparezca y sea interactiva
ventana.mainloop()