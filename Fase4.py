import tkinter as tk

from tkinter import messagebox

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(valor, self.raiz, 1)

    def _insertar_recursivo(self, valor, nodo_actual, nivel):
        if valor < nodo_actual.valor:
            if nodo_actual.izq is None:
                if nivel < 4:
                    nodo_actual.izq = Nodo(valor)
                else:
                    raise Exception("No se pueden agregar mas niveles. Maximo 4 niveles permitidos.")
            else:
                self._insertar_recursivo(valor, nodo_actual.izq, nivel + 1)
        elif valor > nodo_actual.valor:
            if nodo_actual.der is None:
                if nivel < 4:
                    nodo_actual.der = Nodo(valor)
                else:
                    raise Exception("No se pueden agregar mas niveles. Maximo 4 niveles permitidos.")
            else:
                self._insertar_recursivo(valor, nodo_actual.der, nivel + 1)
        # Si el valor ya existe, no hacemos nada

    def buscar(self, valor):
        return self._buscar_recursivo(valor, self.raiz)

    def _buscar_recursivo(self, valor, nodo_actual):
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(valor, nodo_actual.izq)
        return self._buscar_recursivo(valor, nodo_actual.der)

    def limpiar(self):
        self.raiz = None

    def preorden(self, nodo, resultado):
        if nodo:
            resultado.append(str(nodo.valor))
            self.preorden(nodo.izq, resultado)
            self.preorden(nodo.der, resultado)

    def inorden(self, nodo, resultado):
        if nodo:
            self.inorden(nodo.izq, resultado)
            resultado.append(str(nodo.valor))
            self.inorden(nodo.der, resultado)

    def postorden(self, nodo, resultado):
        if nodo:
            self.postorden(nodo.izq, resultado)
            self.postorden(nodo.der, resultado)
            resultado.append(str(nodo.valor))

def dibujar_lineas(canvas, nodo, x, y, dx):
    """Dibuja solo las lineas del arbol."""
    if nodo is not None:
        if nodo.izq:
            canvas.create_line(x, y, x - dx, y + 80, width=2, fill="black")
            dibujar_lineas(canvas, nodo.izq, x - dx, y + 80, dx / 2)
        if nodo.der:
            canvas.create_line(x, y, x + dx, y + 80, width=2, fill="black")
            dibujar_lineas(canvas, nodo.der, x + dx, y + 80, dx / 2)

def dibujar_nodos(canvas, nodo, x, y, dx):
    """Dibuja los circulos de los nodos y su valor, encima de las lineas."""
    if nodo is not None:
        radio = 20
        # Llamadas recursivas a los hijos
        if nodo.izq:
            dibujar_nodos(canvas, nodo.izq, x - dx, y + 80, dx / 2)
        if nodo.der:
            dibujar_nodos(canvas, nodo.der, x + dx, y + 80, dx / 2)
        
        # Dibujar circulo del nodo actual y el texto
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(nodo.valor), font=("Helvetica", 12, "bold"))

def abrir_arbol_binario():
    arbol_binario_ventana = tk.Tk()
    arbol_binario_ventana.title("Arbol Binario")
    arbol_binario_ventana.geometry("1300x650")
    arbol_binario_ventana.resizable(False, False)

    # Instancia del arbol
    arbol = ArbolBinario()

    # --- Frame Superior para controles ---
    frame_controles = tk.Frame(arbol_binario_ventana)
    frame_controles.pack(pady=10, fill='x')

    tk.Label(frame_controles, text="Nodo (Entero):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    entry_nodo = tk.Entry(frame_controles, font=("Helvetica", 12), width=10)
    entry_nodo.pack(side=tk.LEFT, padx=5)

    def actualizar_graficos():
        canvas_arbol.delete("all")
        if arbol.raiz:
            # Empezamos a dibujar desde el centro superior
            dibujar_lineas(canvas_arbol, arbol.raiz, 650, 50, 300)
            dibujar_nodos(canvas_arbol, arbol.raiz, 650, 50, 300)
            
        # Actualizar recorridos
        res_pre = []
        arbol.preorden(arbol.raiz, res_pre)
        label_preorden.config(text="Preorden: " + " - ".join(res_pre))

        res_in = []
        arbol.inorden(arbol.raiz, res_in)
        label_inorden.config(text="Inorden: " + " - ".join(res_in))

        res_pos = []
        arbol.postorden(arbol.raiz, res_pos)
        label_postorden.config(text="Postorden: " + " - ".join(res_pos))

    def agregar_nodo():
        try:
            valor = int(entry_nodo.get())
            try:
                arbol.insertar(valor)
                actualizar_graficos()
                entry_nodo.delete(0, tk.END)
            except Exception as e:
                messagebox.showwarning("Limite Alcanzado", str(e))
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor entero valido.")

    def buscar_nodo():
        try:
            valor = int(entry_nodo.get())
            encontrado = arbol.buscar(valor)
            if encontrado:
                messagebox.showinfo("Resultado", f"El nodo {valor} se encuentra en el arbol.")
            else:
                messagebox.showinfo("Resultado", f"El nodo {valor} NO se encuentra en el arbol.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor entero valido.")

    def limpiar_arbol():
        arbol.limpiar()
        actualizar_graficos()

    tk.Button(frame_controles, text="Agregar Nodo", command=agregar_nodo, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_controles, text="Buscar Nodo", command=buscar_nodo, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_controles, text="Limpiar", command=limpiar_arbol, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_controles, text="Salir", command=arbol_binario_ventana.destroy, font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=20)

    # --- Canvas Principal para el Arbol ---
    canvas_arbol = tk.Canvas(arbol_binario_ventana, width=1280, height=450, bg="white", relief=tk.SUNKEN, bd=2)
    canvas_arbol.pack(pady=10)

    # --- Frame Inferior para Recorridos ---
    frame_recorridos = tk.Frame(arbol_binario_ventana)
    frame_recorridos.pack(fill='x', padx=20, pady=10)

    # 3 paneles (LabelFrames)
    panel_preorden = tk.LabelFrame(frame_recorridos, text="Recorrido Preorden", font=("Helvetica", 10, "bold"), fg="cyan")
    panel_preorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    label_preorden = tk.Label(panel_preorden, text="Preorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_preorden.pack(pady=10, padx=10, anchor="w")

    panel_inorden = tk.LabelFrame(frame_recorridos, text="Recorrido Inorden", font=("Helvetica", 10, "bold"), fg="green")
    panel_inorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    label_inorden = tk.Label(panel_inorden, text="Inorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_inorden.pack(pady=10, padx=10, anchor="w")

    panel_postorden = tk.LabelFrame(frame_recorridos, text="Recorrido Postorden", font=("Helvetica", 10, "bold"), fg="red")
    panel_postorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    label_postorden = tk.Label(panel_postorden, text="Postorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_postorden.pack(pady=10, padx=10, anchor="w")

def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculacion con eventos de teclado.
    """
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "ARBOL":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Cierra la ventana de login
        abrir_arbol_binario()
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            messagebox.showwarning("Acceso Denegado", f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END) # Limpia el campo de contraseña
        else:
            messagebox.showerror("Acceso Bloqueado", "Ha superado el número de intentos permitidos.", parent=ventana)
            ventana.destroy() # Cierra la aplicación


ventana = tk.Tk()
ventana.title("Fase 4 — Juan Garcia")
ventana.geometry("500x250")
ventana.resizable(False, False)

# --- Creación de Widgets ---
tk.Label(ventana, text="Aplicacion Arboles Binarios").pack(pady=5)
tk.Label(ventana, text="Estudiante: Juan Garcia").pack(pady=3)
tk.Label(ventana, text="Fecha: 10/05/2026").pack(pady=3)
tk.Label(ventana, text="Ingrese la contraseña de acceso:").pack(pady=3)

# Este es el campo de entrada para la contraseña. La opción show="*" oculta el texto.
entry_contrasena = tk.Entry(ventana, show="-", font=("Helvetica", 12), width=25)
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