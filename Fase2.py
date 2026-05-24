import tkinter as tk

from tkinter import messagebox
from tkinter import ttk # Importar ttk para el Combobox
from datetime import date

class GestionEmpleados:
    """Clase para gestionar los registros de los empleados."""
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado_data):
        """Añade un diccionario de datos de empleado a la lista."""
        self.empleados.append(empleado_data)
        print("--- Registro Guardado ---")
        print(empleado_data)
        print(f"Total de registros actuales: {len(self.empleados)}")

# Creamos una instancia única para gestionar a todos los empleados
gestion = GestionEmpleados()

def abrir_ventana_registro(parent=None):
    """Crea y muestra la ventana principal para el registro de empleados."""
    if parent:
        registro = tk.Toplevel(parent)
    else:
        registro = tk.Tk()
    registro.title("Registro y Nómina de Empleados")
    registro.geometry("450x380") # Ajustamos la altura para los campos visibles
    registro.resizable(False, False)

    # Usamos un Frame para agrupar los widgets del formulario y darles un padding
    frame_formulario = tk.Frame(registro, padx=15, pady=15)
    frame_formulario.pack(fill="both", expand=True)

    # --- Configuración del Grid ---
    # Hacemos que la columna 1 (donde irán los Entry) se expanda para llenar el espacio
    frame_formulario.columnconfigure(1, weight=1)

    # --- Datos para el formulario ---
    salarios = {
        "Servicios generales": 40000,
        "Administrativo": 50000,
        "Electricista": 60000,
        "Mecanico": 80000,
        "Soldador": 90000
    }
    cargos = list(salarios.keys())
    labels_texto = ["Identificacion:", "Nombre Completo:", "Genero:", "Cargo Laboral:", "Salario Dia:", "Dias Laborados:"]

    # --- Variables de Control de Tkinter ---
    genero_var = tk.StringVar()
    salario_var = tk.StringVar()

    # Diccionario para mantener referencias a los widgets de entrada
    form_widgets = {}

    # --- Función de validación para permitir solo números ---
    def validar_solo_numeros(P):
        # %P es el valor que tendrá el Entry si se permite la edición.
        # Permitir un campo vacío o un campo que contenga solo dígitos.
        return P == "" or P.isdigit()
    vcmd = (registro.register(validar_solo_numeros), '%P')

    # --- Función para actualizar el salario basado en el cargo ---
    def actualizar_salario(event=None):
        cargo_seleccionado = combo_cargo.get()
        if cargo_seleccionado:
            salario_dia = salarios.get(cargo_seleccionado, 0)
            salario_formateado = f"${salario_dia:,.0f}"
            salario_var.set(salario_formateado)
        else:
            salario_var.set("") # Dejar en blanco si no hay selección

    def guardar_registro():
        try:
            # Recopilar datos de los widgets
            identificacion = form_widgets['identificacion'].get()
            nombre = form_widgets['nombre_completo'].get()
            genero = form_widgets['genero'].get()
            cargo = form_widgets['cargo'].get()
            dias_laborados_str = form_widgets['dias_laborados'].get()

            # Validar que los campos no estén vacíos
            if not all([identificacion, nombre, genero, cargo, dias_laborados_str]):
                messagebox.showwarning("Campos Incompletos", "Por favor, rellene todos los campos obligatorios.")
                return

            dias_laborados = int(dias_laborados_str)

            # Validar que los días laborados estén en el rango de 1 a 30
            if not (1 <= dias_laborados <= 30):
                messagebox.showwarning("Dato Inválido", "Los días laborados deben ser un número entre 1 y 30.")
                return

            salario_dia = salarios.get(cargo, 0)
            
            # Crear el diccionario de datos del empleado
            empleado_data = {
                "identificacion": identificacion, "nombre": nombre, "genero": genero,
                "cargo": cargo, "salario_dia": salario_dia, "dias_laborados": dias_laborados,
                "fecha_registro": date.today().strftime("%d/%m/%Y"),
                "total_a_pagar": salario_dia * dias_laborados
            }

            # Usar la instancia de GestionEmpleados para guardar el registro
            gestion.agregar_empleado(empleado_data)
            messagebox.showinfo("Registro Exitoso", f"Empleado '{nombre}' ha sido guardado correctamente.")

            # Limpiar formulario para el siguiente registro
            form_widgets['identificacion'].delete(0, tk.END)
            form_widgets['nombre_completo'].delete(0, tk.END)
            form_widgets['dias_laborados'].delete(0, tk.END)
            form_widgets['cargo'].set('')
            actualizar_salario() # Limpia la etiqueta del salario

        except ValueError:
            messagebox.showerror("Error de Datos", "El campo 'Días Laborados' debe ser un número entero válido.")

    def mostrar_reporte():
        """Muestra un reporte. Si hay empleados guardados, muestra una nómina general.
        Si no, muestra un cálculo basado en los datos del formulario."""
        if not gestion.empleados:
            # --- Reporte desde el formulario (si no hay registros) ---
            try:
                # Recopilar datos de los widgets
                identificacion = form_widgets['identificacion'].get()
                nombre = form_widgets['nombre_completo'].get()
                genero = form_widgets['genero'].get()
                cargo = form_widgets['cargo'].get()
                dias_laborados_str = form_widgets['dias_laborados'].get()

                # Validar que los campos no estén vacíos
                if not all([identificacion, nombre, genero, cargo, dias_laborados_str]):
                    messagebox.showwarning("Campos Incompletos", "Para generar un reporte del formulario, por favor, rellene todos los campos.")
                    return

                dias_laborados = int(dias_laborados_str)
                # Validar que los días laborados estén en el rango de 1 a 30
                if not (1 <= dias_laborados <= 30):
                    messagebox.showwarning("Dato Inválido", "Para generar el reporte, los días laborados deben ser un número entre 1 y 30.")
                    return

                salario_dia = salarios.get(cargo, 0)
                total_a_pagar = salario_dia * dias_laborados

                # Crear el contenido del reporte
                reporte_contenido = f"--- Reporte de Empleado (No Guardado) ---\n\n"
                reporte_contenido += f"Identificación: {identificacion}\n"
                reporte_contenido += f"Nombre: {nombre}\n"
                reporte_contenido += f"Cargo: {cargo}\n"
                reporte_contenido += f"Días Laborados: {dias_laborados}\n"
                reporte_contenido += f"Salario por Día: ${salario_dia:,.0f}\n"
                reporte_contenido += f"Total a Pagar: ${total_a_pagar:,.0f}\n"

                messagebox.showinfo("Reporte de Formulario", reporte_contenido)

            except ValueError:
                messagebox.showerror("Error de Datos", "El campo 'Días Laborados' debe ser un número entero válido para generar el reporte.")
        else:
            # --- Reporte de todos los empleados guardados ---
            ventana_reporte = tk.Toplevel(registro)
            ventana_reporte.title("Reporte de Nómina General")
            ventana_reporte.geometry("900x450")

            texto_reporte = tk.Text(ventana_reporte, wrap="none", font=("Courier", 14))
            texto_reporte.pack(padx=10, pady=10, fill="both", expand=True)

            reporte_contenido = "--- Reporte General de Nómina ---\n\n"
            total_nomina = 0

            # Encabezados
            reporte_contenido += f"{'ID':<15} {'Nombre':<25} {'Cargo':<20} {'Fecha Registro':<15} {'Total a Pagar':>18}\n"
            reporte_contenido += "="*97 + "\n"

            for emp in gestion.empleados:
                total_a_pagar = emp.get('total_a_pagar', 0)
                total_nomina += total_a_pagar
                reporte_contenido += f"{emp.get('identificacion', ''):<15} {emp.get('nombre', ''):<25} {emp.get('cargo', ''):<20} {emp.get('fecha_registro', ''):<15} ${total_a_pagar:>17,.0f}\n"

            reporte_contenido += "\n" + "="*97 + "\n"
            reporte_contenido += f"TOTAL NÓMINA: ${total_nomina:,.0f}\n"
            reporte_contenido += f"TOTAL EMPLEADOS: {len(gestion.empleados)}\n"

            texto_reporte.insert(tk.END, reporte_contenido)
            texto_reporte.config(state="disabled") # Hacer el texto de solo lectura

    for i, texto in enumerate(labels_texto):
        # Label a la izquierda (columna 0)
        label = tk.Label(frame_formulario, text=texto, font=("Helvetica", 12))
        label.grid(row=i, column=0, padx=5, pady=8, sticky="w") # sticky="w" (West) alinea a la izquierda

        if texto == "Genero:":
            # Usamos un Frame para agrupar los Radiobutton
            frame_genero = tk.Frame(frame_formulario)
            frame_genero.grid(row=i, column=1, padx=5, pady=8, sticky="w")
            
            rb_masculino = tk.Radiobutton(frame_genero, text="Masculino", variable=genero_var, value="Masculino", font=("Helvetica", 11))
            rb_masculino.pack(side="left")
            
            rb_femenino = tk.Radiobutton(frame_genero, text="Femenino", variable=genero_var, value="Femenino", font=("Helvetica", 11))
            rb_femenino.pack(side="left", padx=10)
            
            genero_var.set("Masculino")
            form_widgets['genero'] = genero_var

        elif texto == "Cargo Laboral:":
            # Usamos un Combobox (dropdown) para los cargos
            combo_cargo = ttk.Combobox(frame_formulario, values=cargos, font=("Helvetica", 12), state="readonly")
            combo_cargo.grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            combo_cargo.bind("<<ComboboxSelected>>", actualizar_salario) # Vincula el evento a la función
            form_widgets['cargo'] = combo_cargo
        
        elif texto == "Salario Dia:":
            # Label para mostrar el salario (solo lectura)
            label_valor_salario = tk.Label(frame_formulario, textvariable=salario_var, font=("Helvetica", 12, "bold"))
            label_valor_salario.grid(row=i, column=1, padx=5, pady=8, sticky="w")

        elif texto == "Dias Laborados:":
            entry = tk.Entry(frame_formulario, font=("Helvetica", 12), validate="key", validatecommand=vcmd)
            entry.grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            form_widgets['dias_laborados'] = entry

        else:
            # Entry para Identificacion y Nombre Completo
            entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
            if texto == "Identificacion:":
                entry.config(validate="key", validatecommand=vcmd)
            entry.grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            key = texto.lower().replace(":", "").replace(" ", "_")
            form_widgets[key] = entry

    # --- Botones de Acción ---
    frame_botones = tk.Frame(frame_formulario)
    frame_botones.grid(row=len(labels_texto), column=0, columnspan=2, pady=20)
    tk.Button(frame_botones, text="Guardar Registro", command=guardar_registro, font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Calcular Nómina / Mostrar Reporte", command=mostrar_reporte, font=("Helvetica", 12)).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Salir", command=registro.destroy, font=("Helvetica", 12)).grid(row=0, column=2, padx=5)

    # Llamamos a la función una vez al inicio para establecer el valor inicial del salario
    actualizar_salario()

    # Inicia el bucle para esta nueva ventana
    if not isinstance(registro, tk.Toplevel):
        registro.mainloop()
    return registro