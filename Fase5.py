import tkinter as tk
from tkinter import messagebox

# Import dynamic launch functions from each phase
from Fase2 import abrir_ventana_registro
from Fase3 import abrir_control_afiliados
from Fase4 import abrir_arbol_binario

def menu_principal():
    ventana_menu = tk.Toplevel(ventana)
    ventana_menu.title("Menú Principal — Juan Garcia")
    ventana_menu.geometry("500x420")
    ventana_menu.resizable(False, False)

    # Hook the close button of the menu to close the entire application
    def cerrar_todo():
        ventana.destroy()
    ventana_menu.protocol("WM_DELETE_WINDOW", cerrar_todo)

    # Header Frame
    header_frame = tk.Frame(ventana_menu, height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="ESTRUCTURAS DE DATOS",
        font=("Helvetica", 16, "bold")
    ).pack(pady=(12, 2))

    tk.Label(
        header_frame,
        text="Evaluación Final — Menú Principal",
        font=("Helvetica", 10, "italic")
    ).pack()

    # Content Frame
    content_frame = tk.Frame(ventana_menu)
    content_frame.pack(pady=20, fill="both", expand=True, padx=40)

    # Launch Actions
    def lanzar_fase2():
        ventana_menu.withdraw()
        try:
            fase2_win = abrir_ventana_registro(parent=ventana_menu)
            def al_cerrar():
                fase2_win.destroy()
                ventana_menu.deiconify()
            fase2_win.protocol("WM_DELETE_WINDOW", al_cerrar)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la Fase 2: {e}")
            ventana_menu.deiconify()

    def lanzar_fase3():
        ventana_menu.withdraw()
        try:
            fase3_win = abrir_control_afiliados(parent=ventana_menu)
            def al_cerrar():
                fase3_win.destroy()
                ventana_menu.deiconify()
            fase3_win.protocol("WM_DELETE_WINDOW", al_cerrar)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la Fase 3: {e}")
            ventana_menu.deiconify()

    def lanzar_fase4():
        ventana_menu.withdraw()
        try:
            fase4_win = abrir_arbol_binario(parent=ventana_menu)
            def al_cerrar():
                fase4_win.destroy()
                ventana_menu.deiconify()
            fase4_win.protocol("WM_DELETE_WINDOW", al_cerrar)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la Fase 4: {e}")
            ventana_menu.deiconify()

    def salir():
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea salir del programa?", parent=ventana_menu):
            ventana.destroy()

    # Buttons
    btn_style = {
        "font": ("Helvetica", 11, "bold"),
        "relief": "flat",
        "bd": 0,
        "pady": 8,
        "cursor": "hand2"
    }

    # Custom button generator to add hover effects easily in vanilla Tkinter
    def crear_boton(parent_widget, text, command, bg_color, hover_color):
        btn = tk.Button(parent_widget, text=text, command=command, bg=bg_color, activebackground=hover_color, activeforeground="white", **btn_style)
        btn.config(highlightbackground=bg_color)
        
        # Hover effect functions
        def on_enter(e):
            btn.config(bg=hover_color, highlightbackground=hover_color)
        def on_leave(e):
            btn.config(bg=bg_color, highlightbackground=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    btn_fase2 = crear_boton(content_frame, "Fase 2: Registro de Empleados", lanzar_fase2, "#2980b9", "#3498db")
    btn_fase2.pack(fill="x", pady=6)

    btn_fase3 = crear_boton(content_frame, "Fase 3: Control de Afiliados", lanzar_fase3, "#27ae60", "#2ecc71")
    btn_fase3.pack(fill="x", pady=6)

    btn_fase4 = crear_boton(content_frame, "Fase 4: Árbol Binario", lanzar_fase4, "#8e44ad", "#9b59b6")
    btn_fase4.pack(fill="x", pady=6)

    btn_salir = crear_boton(content_frame, "Salir", salir, "#c0392b", "#e74c3c")
    btn_salir.pack(fill="x", pady=(15, 6))

    # Footer/Developer Frame
    footer_frame = tk.Frame(ventana_menu)
    footer_frame.pack(side="bottom", fill="x", pady=10)
    tk.Label(
        footer_frame,
        text="Estudiante: Juan Garcia  |  Grupo: 301305A_2201",
        font=("Helvetica", 9),
    ).pack()


def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculacion con eventos de teclado.
    """
    try:
        intentos_restantes = int(label_intentos.cget("text").split()[-1])
    except ValueError:
        intentos_restantes = 3
    
    if entry_contrasena.get() == "8246":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.withdraw()  # Hide the login window
        menu_principal()
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            messagebox.showwarning("Acceso Denegado", f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END)  # Limpia el campo de contraseña
        else:
            messagebox.showerror("Acceso Bloqueado", "Ha superado el número de intentos permitidos.", parent=ventana)
            ventana.destroy()  # Cierra la aplicación


ventana = tk.Tk()
ventana.title("Evaluacion Final — Juan Garcia")
ventana.geometry("500x270")
ventana.resizable(False, False)

# --- Creación de Widgets ---
tk.Label(ventana, text="EVALUACIÓN FINAL", font=("Helvetica", 14, "bold")).pack(pady=(15, 5))
tk.Label(ventana, text="Estudiante: Juan Garcia", font=("Helvetica", 10)).pack(pady=2)
tk.Label(ventana, text="Fecha: 24/05/2026", font=("Helvetica", 10)).pack(pady=2)
tk.Label(ventana, text="Ingrese la contraseña de acceso:", font=("Helvetica", 11)).pack(pady=(10, 5))

# Este es el campo de entrada para la contraseña. La opción show="*" oculta el texto.
entry_contrasena = tk.Entry(ventana, show="*", font=("Helvetica", 12), width=25)
entry_contrasena.pack(pady=5)
# Vinculamos la tecla "Enter" (Return) al campo de contraseña para llamar a la función de verificación.
entry_contrasena.bind('<Return>', verificar_contrasena)

label_intentos = tk.Label(ventana, text="Intentos restantes: 3", font=("Helvetica", 10))
label_intentos.pack(pady=5)

# --- Contenedor para los botones ---
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

btn_style = {
    "font": ("Helvetica", 11, "bold"),
    "fg": "white",
    "relief": "flat",
    "bd": 0,
    "padx": 15,
    "pady": 6,
    "cursor": "hand2"
}

def crear_boton_login(parent_widget, text, command):
    btn = tk.Button(parent_widget, text=text, command=command, bg="#2ecc71", activebackground="#27ae60", activeforeground="white", **btn_style)
    def on_enter(e):
        btn.config(bg="#27ae60")
    def on_leave(e):
        btn.config(bg="#2ecc71")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

btn_ingresar = crear_boton_login(frame_botones, "Ingresar", verificar_contrasena)
btn_ingresar.grid(row=0, column=0, padx=10)

btn_salir = crear_boton_login(frame_botones, "Salir", ventana.destroy)
btn_salir.grid(row=0, column=1, padx=10)

# Iniciar el bucle de eventos para que la ventana aparezca y sea interactiva
ventana.mainloop()