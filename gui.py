# gui.py
# Interfaz gráfica principal del Laboratorio 1 - Árbol AVL
# Autores: [Santiago Orozoco,Juan Salcedo, Keymer Perez]
# Sección documentada por: Santiago Orozco

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import os

from avl_tree import AVLTree
from data_loader import load_courses


class App(tk.Tk):
    """Ventana principal de la aplicación.
    
    Clase principal de la aplicación. Representa la ventana principal.
    Hereda de tk.Tk, que es la ventana base de Tkinter.
    Al crear un objeto App, se abre la ventana del programa.
    """

    def __init__(self):

        """
        Se ejecuta automáticamente al crear la aplicación.
        Aquí se define el tamaño y título de la ventana,
        y se crean las variables principales que usa el programa.
        """
               
        super().__init__()
        self.title("Árbol AVL - Cursos Udemy | Estructura de Datos II")
        self.geometry("1400x850")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        self.tree = AVLTree()
        self.courses_db = {}
        self.last_results = []
        self.tree_image_path = None
        self.photo_ref = None

        self._build_ui()
        self._log("Bienvenido al Árbol AVL de Cursos Udemy.")
        self._log("Cargue el dataset CSV para comenzar.")

    # ──────────────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────────────

    def _build_ui(self):

        """
        Método principal que ensambla toda la interfaz visual.
        Divide la ventana en cuatro zonas:
          1. Barra superior → título y botón "Cargar CSV"
          2. Panel izquierdo → todos los controles y botones de operaciones
          3. Panel derecho  → canvas donde se dibuja el árbol
          4. Barra inferior → log de actividad (registro de acciones)
        
        Construye todos los widgets de la interfaz.
        """
        # Barra superior
        top_bar = tk.Frame(self, bg="#181825", pady=8)
        top_bar.pack(fill=tk.X)

        tk.Label(top_bar, text="Árbol AVL — Cursos Udemy",
                 bg="#181825", fg="#cdd6f4",
                 font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT, padx=16)

        tk.Button(top_bar, text=" Cargar CSV", command=self._load_csv,
                  bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=8)

        # Panel principal
        main = tk.Frame(self, bg="#1e1e2e")
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Panel izquierdo
        left = tk.Frame(main, bg="#1e1e2e", width=420)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left.pack_propagate(False)

        self._build_operations_panel(left)
        self._build_results_panel(left)

        # Panel derecho (árbol)
        right = tk.Frame(main, bg="#181825", relief=tk.FLAT, bd=2)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_tree_panel(right)

        # Log inferior
        self._build_log_panel()

    def _section(self, parent, title):
        """
        Crea un recuadro con título para agrupar visualmente elementos relacionados.
        Por ejemplo: el recuadro "Insertar por ID" o el de "Eliminar".
        Retorna el recuadro para poder agregarle botones y campos dentro.
        """
        frame = tk.LabelFrame(parent, text=title, bg="#1e1e2e", fg="#89b4fa",
                              font=("Segoe UI", 10, "bold"), pady=4, padx=6,
                              relief=tk.GROOVE, bd=2)
        frame.pack(fill=tk.X, pady=4)
        return frame

    def _btn(self, parent, text, cmd, color="#89b4fa"):

        """
        Crea y retorna un botón con el estilo visual del programa.
        Parámetros:
          - parent: el contenedor donde se coloca el botón
          - text: texto visible en el botón
          - cmd: función que se ejecuta cuando el usuario hace clic
          - color: color de fondo (por defecto azul claro)
        Nota: el botón se crea pero NO se posiciona; hay que llamar .pack() después.
        """
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="#1e1e2e", font=("Segoe UI", 9, "bold"),
                         relief=tk.FLAT, padx=6, pady=3, cursor="hand2")

    def _entry_row(self, parent, label, width=16):
        """
        Crea una fila con una etiqueta a la izquierda y un campo de texto a la derecha.
        Se usa para los campos donde el usuario escribe un ID o un número.
        Retorna el campo de texto (Entry) para poder leer lo que escribe el usuario.
        """
         
        row = tk.Frame(parent, bg="#1e1e2e")
        row.pack(fill=tk.X, pady=1)
        tk.Label(row, text=label, bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 9), width=18, anchor="w").pack(side=tk.LEFT)
        e = tk.Entry(row, width=width, bg="#313244", fg="#cdd6f4",
                     insertbackground="white", relief=tk.FLAT,
                     font=("Segoe UI", 9))
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        return e

    def _build_operations_panel(self, parent):
        """
        Construye el panel de operaciones con tres pestañas:
          - Pestaña "Insertar / Eliminar": agregar o quitar nodos del árbol
          - Pestaña "Buscar": buscar nodos por ID, satisfacción o criterios especiales
          - Pestaña "Recorrido / Nodo": ver recorrido por niveles y operar sobre un nodo seleccionado
        """
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=False, pady=4)

        style = ttk.Style()
        style.configure("TNotebook", background="#1e1e2e")
        style.configure("TNotebook.Tab", background="#313244",
                        foreground="#1e2027", font=("Segoe UI", 9))

        # Tab 1: Insertar / Eliminar
        tab1 = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab1, text="Insertar / Eliminar")

        sec_ins = self._section(tab1, "Insertar por ID")
        self.entry_insert_id = self._entry_row(sec_ins, "ID del curso:")
        self._btn(sec_ins, "Insertar", self._insert_node,
                  "#a6e3a1").pack(pady=3)

        sec_del = self._section(tab1, "Eliminar")
        self.entry_del_id = self._entry_row(sec_del, "ID del curso:")
        self._btn(sec_del, "Eliminar por ID", self._delete_by_id,
                  "#f38ba8").pack(pady=2)
        self.entry_del_sat = self._entry_row(sec_del, "Satisfacción:")
        self._btn(sec_del, "Eliminar por Satisfacción", self._delete_by_sat,
                  "#fab387").pack(pady=2)

        # Tab 2: Buscar
        tab2 = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab2, text="Buscar")

        sec_search = self._section(tab2, "Búsqueda simple")
        self.entry_search_id = self._entry_row(sec_search, "ID del curso:")
        self._btn(sec_search, "Buscar por ID",
                  self._search_by_id).pack(pady=2)
        self.entry_search_sat = self._entry_row(sec_search, "Satisfacción:")
        self._btn(sec_search, "Buscar por Satisfacción",
                  self._search_by_sat).pack(pady=2)

        sec_criteria = self._section(tab2, "Búsqueda por criterios")
        self._btn(sec_criteria, "a. Positivas > Neg+Neutras",
                  self._criteria_a, "#cba6f7").pack(fill=tk.X, pady=1)

        tk.Label(sec_criteria, text="Fecha (YYYY-MM-DD):", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 9)).pack(anchor="w")
        self.entry_date = tk.Entry(sec_criteria, bg="#313244", fg="#cdd6f4",
                                   insertbackground="white", relief=tk.FLAT,
                                   font=("Segoe UI", 9))
        self.entry_date.pack(fill=tk.X, pady=1)
        self._btn(sec_criteria, "b. Creados después de fecha",
                  self._criteria_b, "#cba6f7").pack(fill=tk.X, pady=1)

        tk.Label(sec_criteria, text="Min clases:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 9)).pack(anchor="w")
        self.entry_min_lec = tk.Entry(sec_criteria, bg="#313244", fg="#cdd6f4",
                                      insertbackground="white", relief=tk.FLAT,
                                      font=("Segoe UI", 9))
        self.entry_min_lec.pack(fill=tk.X, pady=1)
        tk.Label(sec_criteria, text="Max clases:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 9)).pack(anchor="w")
        self.entry_max_lec = tk.Entry(sec_criteria, bg="#313244", fg="#cdd6f4",
                                      insertbackground="white", relief=tk.FLAT,
                                      font=("Segoe UI", 9))
        self.entry_max_lec.pack(fill=tk.X, pady=1)
        self._btn(sec_criteria, "c. Clases en rango",
                  self._criteria_c, "#cba6f7").pack(fill=tk.X, pady=1)

        tk.Label(sec_criteria, text="Tipo de reseña:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 9)).pack(anchor="w")
        self.combo_review = ttk.Combobox(
            sec_criteria, values=["positive", "negative", "neutral"],
            state="readonly", width=15)
        self.combo_review.current(0)
        self.combo_review.pack(anchor="w", pady=2)
        self._btn(sec_criteria, "d. Reseñas > promedio",
                  self._criteria_d, "#cba6f7").pack(fill=tk.X, pady=1)

        # Tab 3: Recorrido / Nodo
        tab3 = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab3, text="Recorrido / Nodo")

        self._btn(tab3, "5. Recorrido por niveles (BFS)",
                  self._level_order, "#89dceb").pack(fill=tk.X, pady=4, padx=4)

        sec_node = self._section(tab3, "Operaciones sobre nodo seleccionado")
        tk.Label(sec_node,
                 text="Selecciona un nodo de los resultados\ny usa estas acciones:",
                 bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w")

        ops = [
            ("a. Info completa", self._node_info),
            ("b. Nivel del nodo", self._node_level),
            ("c. Factor de balanceo", self._node_bf),
            ("d. Padre (recursivo)", self._node_parent),
            ("e. Abuelo (recursivo)", self._node_grandparent),
            ("f. Tío (recursivo)", self._node_uncle),
        ]
        for label, cmd in ops:
            self._btn(sec_node, label, cmd, "#f9e2af").pack(fill=tk.X, pady=1)

    def _build_results_panel(self, parent):
        """
        Crea el panel de resultados debajo de las pestañas.
        Muestra una lista con los nodos encontrados después de una búsqueda.
        El usuario puede hacer clic en uno para seleccionarlo
        y luego aplicarle operaciones desde la pestaña 'Recorrido / Nodo'.
        """    
        sec = self._section(parent, "Resultados")
        self.results_list = tk.Listbox(
            sec, bg="#313244", fg="#cdd6f4", font=("Segoe UI", 9), height=8,
            selectbackground="#89b4fa", selectforeground="#1e1e2e",
            relief=tk.FLAT)
        self.results_list.pack(fill=tk.BOTH, expand=True, pady=2)
        scroll = tk.Scrollbar(sec, command=self.results_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_list.config(yscrollcommand=scroll.set)

    def _build_tree_panel(self, parent):

        """
        Crea el panel derecho donde se muestra la imagen del árbol.
        Usa un Canvas (lienzo) con barras de scroll para poder navegar
        cuando el árbol crece y no cabe en pantalla.
        También se puede arrastrar la imagen con el mouse.
        """   
        tk.Label(parent, text="Visualización del Árbol",
                 bg="#181825", fg="#89b4fa",
                 font=("Segoe UI", 11, "bold")).pack(pady=6)

        frame = tk.Frame(parent, bg="#181825")
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg="#181825", cursor="fleur")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL,
                            command=self.canvas.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL,
                            command=self.canvas.xview)
        hbar.pack(fill=tk.X)

        self.canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.canvas.bind("<ButtonPress-1>", self._scroll_start)
        self.canvas.bind("<B1-Motion>", self._scroll_move)

    def _build_log_panel(self):
        """
        Crea la barra de log en la parte inferior de la ventana.
        Registra automáticamente cada acción que hace el usuario:
        inserciones, eliminaciones, búsquedas, errores, etc.
        El usuario no puede escribir en este campo (es solo lectura).
        """
        log_frame = tk.Frame(self, bg="#181825", height=110)
        log_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=4)
        log_frame.pack_propagate(False)

        tk.Label(log_frame, text="Log de actividad",
                 bg="#181825", fg="#89b4fa",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=4)

        self.log_text = tk.Text(
            log_frame, bg="#11111b", fg="#a6e3a1",
            font=("Consolas", 9), height=5,
            relief=tk.FLAT, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4)

    # ──────────────────────────────────────────────────────
    # Scroll del canvas
    # ──────────────────────────────────────────────────────

    def _scroll_start(self, event):
        """Registra la posición del mouse cuando el usuario hace clic en el canvas."""
        self.canvas.scan_mark(event.x, event.y)

    def _scroll_move(self, event):
        """Mueve la imagen del árbol mientras el usuario arrastra el mouse."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # ──────────────────────────────────────────────────────
    # Utilidades
    # ──────────────────────────────────────────────────────

    def _log(self, msg):
        """
        Agrega un mensaje de texto al log de actividad (parte inferior).
        Pasos: habilita el área → escribe → hace scroll al final → vuelve a bloquear.
        Esto evita que el usuario pueda editar el log accidentalmente.
        """  
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"▶ {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _show_results(self, nodes, label="Resultados"):
        """
        Muestra una lista de nodos en el panel de resultados (abajo izquierda).
        También guarda los nodos en self.last_results para poder recuperarlos
        cuando el usuario seleccione uno y quiera ver su información.
        Parámetros:
          - nodes: lista de objetos AVLNode encontrados
          - label: texto descriptivo para el log (ej: "Búsqueda por ID")
        """
        self.last_results = nodes
        self.results_list.delete(0, tk.END)
        for node in nodes:
            c = node.course
            self.results_list.insert(
                tk.END,
                f"ID: {c.id} | Sat: {c.satisfaction} | {c.title[:40]}")
        self._log(f"{label}: {len(nodes)} resultado(s) encontrado(s).")

    def _get_selected_node(self):
        """
        Retorna el nodo que el usuario seleccionó en la lista de resultados.
        Si no hay ningún elemento seleccionado, muestra una advertencia y retorna None.
        Se usa antes de ejecutar operaciones sobre un nodo (padre, abuelo, tío, etc.).
        """
        sel = self.results_list.curselection()
        if not sel:
            messagebox.showwarning(
                "Sin selección",
                "Selecciona un nodo de la lista de resultados.")
            return None
        return self.last_results[sel[0]]

    def _refresh_tree_image(self, highlight_ids=None):
        """
        Genera una nueva imagen del árbol con Graphviz y la muestra en el canvas.
        Lo hace en un hilo separado (threading) para que la interfaz no se congele
        mientras Graphviz procesa y dibuja el árbol.
        Parámetros:
          - highlight_ids: lista de IDs que se quieren resaltar en amarillo en la imagen
        """
        def task():
            path = self.tree.visualize("avl_tree", highlight_ids)
            self.after(0, lambda: self._display_image(path))
        threading.Thread(target=task, daemon=True).start()

    def _display_image(self, path):
        """
        Carga la imagen PNG generada y la muestra en el canvas del panel derecho.
        También actualiza el área de scroll para que el usuario pueda
        navegar por toda la imagen si el árbol es más grande que la pantalla.
        """
        if not os.path.exists(path):
            self._log("No se pudo generar la imagen del árbol.")
            return
        img = Image.open(path)
        self.photo_ref = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_ref)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # ──────────────────────────────────────────────────────
    # Cargar CSV
    # ──────────────────────────────────────────────────────

    def _load_csv(self):
        """
        Abre un explorador de archivos para que el usuario elija el CSV.
        Lee todos los cursos del archivo y los guarda en self.courses_db.
        IMPORTANTE: este método solo carga los datos en memoria,
        NO los inserta en el árbol. Eso lo hace el usuario manualmente.
        """
        path = filedialog.askopenfilename(
            title="Seleccionar dataset CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        self._log(f"Cargando {os.path.basename(path)}...")
        self.update()
        try:
            self.courses_db = load_courses(path)
            self._log(f"{len(self.courses_db)} cursos cargados en memoria.")
            messagebox.showinfo(
                "Carga exitosa",
                f"{len(self.courses_db)} cursos cargados correctamente.\n"
                "Ahora puede insertar nodos por ID.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el CSV:\n{e}")

    # ──────────────────────────────────────────────────────
    # Operación 1 — Insertar
    # ──────────────────────────────────────────────────────

    def _insert_node(self):
        """
        Lee el ID escrito por el usuario en el campo de inserción,
        busca ese curso en self.courses_db (el CSV cargado),
        y lo inserta en el árbol AVL.
        Después regenera la imagen visual del árbol.
        Valida que el campo no esté vacío y que el ID sea un número entero válido.
        """       
        raw = self.entry_insert_id.get().strip()
        if not raw:
            messagebox.showwarning("Campo vacío", "Ingresa el ID del curso.")
            return
        try:
            cid = int(raw)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        if cid not in self.courses_db:
            messagebox.showerror(
                "No encontrado",
                f"El ID {cid} no existe en el dataset cargado.")
            return
        self.tree.insert(self.courses_db[cid])
        self._log(
            f"Insertado: ID={cid} | Sat={self.courses_db[cid].satisfaction}")
        self._refresh_tree_image()

    # ──────────────────────────────────────────────────────
    # Operación 2 — Eliminar
    # ──────────────────────────────────────────────────────

    def _delete_by_id(self):
        """
        Elimina del árbol el nodo que tenga el ID ingresado por el usuario.
        El árbol se rebalancea automáticamente después de eliminar.
        Si el ID no existe en el árbol, muestra un aviso.
        """        
        raw = self.entry_del_id.get().strip()
        if not raw:
            messagebox.showwarning("Campo vacío", "Ingresa el ID.")
            return
        try:
            cid = int(raw)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        ok = self.tree.delete_by_id(cid)
        if ok:
            self._log(f"Eliminado nodo con ID={cid}")
            self._refresh_tree_image()
        else:
            messagebox.showinfo("No encontrado",
                                f"ID {cid} no está en el árbol.")

    def _delete_by_sat(self):
        """
        Elimina del árbol el nodo con el nivel de satisfacción ingresado.
        Si hay varios nodos con exactamente la misma satisfacción,
        elimina el primero que encuentre.
        """
        
        raw = self.entry_del_sat.get().strip()
        if not raw:
            messagebox.showwarning("Campo vacío", "Ingresa la satisfacción.")
            return
        try:
            sat = float(raw)
        except ValueError:
            messagebox.showerror("Error",
                                 "La satisfacción debe ser un número.")
            return
        ok = self.tree.delete_by_satisfaction(sat)
        if ok:
            self._log(f"Eliminado nodo con satisfacción={sat}")
            self._refresh_tree_image()
        else:
            messagebox.showinfo("No encontrado",
                                f"Satisfacción {sat} no está en el árbol.")

    # ──────────────────────────────────────────────────────
    # Operación 3 — Buscar
    # ──────────────────────────────────────────────────────

    def _search_by_id(self):
        """
        Busca en el árbol el nodo con el ID exacto ingresado.
        Si lo encuentra:
          - Lo muestra en la lista de resultados
          - Lo resalta en amarillo en la imagen del árbol
        """        
        raw = self.entry_search_id.get().strip()
        if not raw:
            messagebox.showwarning("Campo vacío", "Ingresa el ID.")
            return
        try:
            cid = int(raw)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        node = self.tree.search_by_id(cid)
        if node:
            self._show_results([node], "Búsqueda por ID")
            self._refresh_tree_image(highlight_ids=[cid])
        else:
            messagebox.showinfo("No encontrado",
                                f"ID {cid} no está en el árbol.")

    def _search_by_sat(self):
        """
        Busca todos los nodos que tengan exactamente el nivel de satisfacción ingresado.
        Pueden aparecer varios resultados si hay cursos con la misma satisfacción.
        Todos los nodos encontrados se resaltan en amarillo en el árbol.
        """       
        raw = self.entry_search_sat.get().strip()
        if not raw:
            messagebox.showwarning("Campo vacío", "Ingresa la satisfacción.")
            return
        try:
            sat = float(raw)
        except ValueError:
            messagebox.showerror("Error",
                                 "La satisfacción debe ser un número.")
            return
        nodes = self.tree.search_by_satisfaction(sat)
        self._show_results(nodes, "Búsqueda por satisfacción")
        if nodes:
            self._refresh_tree_image(
                highlight_ids=[n.course.id for n in nodes])

    # ──────────────────────────────────────────────────────
    # Operación 4 — Criterios
    # ──────────────────────────────────────────────────────

    def _criteria_a(self):
        """
        Criterio a: encuentra los cursos del árbol donde
        reseñas_positivas > reseñas_negativas + reseñas_neutras.
        Resalta los resultados en amarillo en el árbol.
        """        
        nodes = self.tree.search_positive_greater_than_neg_plus_neutral()
        self._show_results(nodes, "Criterio 4a")
        if nodes:
            self._refresh_tree_image(
                highlight_ids=[n.course.id for n in nodes])

    def _criteria_b(self):
        """
        Criterio b: encuentra los cursos creados DESPUÉS de la fecha ingresada.
        El formato de fecha debe ser YYYY-MM-DD (ej: 2020-06-15).
        """        
        date = self.entry_date.get().strip()
        if not date:
            messagebox.showwarning("Campo vacío",
                                   "Ingresa una fecha (YYYY-MM-DD).")
            return
        nodes = self.tree.search_created_after(date)
        self._show_results(nodes, f"Criterio 4b (después de {date})")
        if nodes:
            self._refresh_tree_image(
                highlight_ids=[n.course.id for n in nodes])

    def _criteria_c(self):
        """
        Criterio 4c: encuentra los cursos cuya cantidad de clases publicadas
        está dentro del rango [min_clases, max_clases] ingresado por el usuario.
        Ejemplo: entre 50 y 200 clases.
        """        
        try:
            mn = int(self.entry_min_lec.get().strip())
            mx = int(self.entry_max_lec.get().strip())
        except ValueError:
            messagebox.showerror("Error",
                                 "Los valores de rango deben ser enteros.")
            return
        nodes = self.tree.search_lectures_in_range(mn, mx)
        self._show_results(nodes, f"Criterio 4c [{mn}-{mx} clases]")
        if nodes:
            self._refresh_tree_image(
                highlight_ids=[n.course.id for n in nodes])

    def _criteria_d(self):
        """
        Criterio 4d: encuentra los cursos donde el tipo de reseña seleccionado
        (positiva, negativa o neutra) es mayor al promedio de todos los nodos del árbol.
        El tipo se elige en el menú desplegable (combo_review).
        """

        rtype = self.combo_review.get()
        nodes = self.tree.search_reviews_above_average(rtype)
        self._show_results(nodes, f"Criterio 4d ({rtype} > promedio)")
        if nodes:
            self._refresh_tree_image(
                highlight_ids=[n.course.id for n in nodes])

    # ──────────────────────────────────────────────────────
    # Operación 5 — Recorrido por niveles
    # ──────────────────────────────────────────────────────

    def _level_order(self):
        """
        Muestra el recorrido por niveles del árbol en una ventana emergente.
        El BFS visita todos los nodos de izquierda a derecha, nivel por nivel:
          Nivel 1 → la raíz
          Nivel 2 → los hijos de la raíz
          Nivel 3 → los nietos de la raíz, etc.
        Solo muestra los IDs de los cursos, tal como pide el laboratorio.
        """    
        levels = self.tree.level_order()
        if not levels:
            messagebox.showinfo("Árbol vacío", "El árbol está vacío.")
            return
        win = tk.Toplevel(self)
        win.title("Recorrido por Niveles")
        win.geometry("500x400")
        win.configure(bg="#1e1e2e")

        tk.Label(win, text="Recorrido por Niveles",
                 bg="#1e1e2e", fg="#89b4fa",
                 font=("Segoe UI", 12, "bold")).pack(pady=8)

        text = tk.Text(win, bg="#313244", fg="#cdd6f4",
                       font=("Consolas", 10), relief=tk.FLAT)
        text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        for i, level in enumerate(levels):
            text.insert(tk.END, f"Nivel {i+1}: {level}\n")
        text.config(state=tk.DISABLED)

    # ──────────────────────────────────────────────────────
    # Operaciones sobre nodo seleccionado
    # ──────────────────────────────────────────────────────

    def _node_info(self):
        """
        Muestra en una ventana emergente TODA la información del curso
        del nodo seleccionado: título, URL, rating, satisfacción,
        cantidad de reseñas, fechas, duración, instructor, etc.
        """        
        node = self._get_selected_node()
        if not node:
            return
        win = tk.Toplevel(self)
        win.title(f"Info del curso ID={node.course.id}")
        win.geometry("480x380")
        win.configure(bg="#1e1e2e")

        tk.Label(win, text="Información del Curso",
                 bg="#1e1e2e", fg="#89b4fa",
                 font=("Segoe UI", 12, "bold")).pack(pady=8)

        text = tk.Text(win, bg="#313244", fg="#cdd6f4",
                       font=("Consolas", 10), relief=tk.FLAT)
        text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        text.insert(tk.END, str(node.course))
        text.config(state=tk.DISABLED)

    def _node_level(self):
        """
        Muestra en qué nivel del árbol se encuentra el nodo seleccionado.
        La raíz siempre está en el nivel 1.
        Un hijo de la raíz está en el nivel 2, y así sucesivamente.
        """        
        node = self._get_selected_node()
        if not node:
            return
        level = self.tree.get_node_level(node)
        self._log(f"Nivel del nodo ID={node.course.id}: {level}")
        messagebox.showinfo("Nivel del nodo",
                            f"El nodo ID={node.course.id} está en el nivel {level}.")

    def _node_bf(self):
        """
        Muestra el factor de balanceo del nodo seleccionado.
        Factor de balanceo = altura(subárbol izquierdo) - altura(subárbol derecho).
        En un árbol AVL válido, este valor siempre es -1, 0 o 1.
        Si es 0: ambos lados tienen la misma altura.
        Si es 1: el lado izquierdo es un nivel más alto.
        Si es -1: el lado derecho es un nivel más alto.
        """        
        node = self._get_selected_node()
        if not node:
            return
        bf = self.tree.get_node_balance_factor(node)
        self._log(f"Factor de balanceo nodo ID={node.course.id}: {bf}")
        messagebox.showinfo("Factor de balanceo",
                            f"Nodo ID={node.course.id}\nFactor de balanceo: {bf}")

    def _node_parent(self):
        """
        Encuentra y muestra el nodo PADRE del nodo seleccionado.
        El padre es el nodo que está un nivel arriba y tiene al nodo
        seleccionado como hijo izquierdo o derecho.
        La búsqueda se realiza de forma recursiva desde la raíz.
        Si el nodo seleccionado ES la raíz, no tiene padre.
        """        
        node = self._get_selected_node()
        if not node:
            return
        parent = self.tree.get_parent(node)
        if parent:
            self._log(f"Padre de ID={node.course.id}: ID={parent.course.id}")
            messagebox.showinfo(
                "Padre",
                f"Padre del nodo ID={node.course.id}:\n"
                f"ID={parent.course.id} | {parent.course.title[:50]}")
        else:
            messagebox.showinfo("Sin padre",
                                f"El nodo ID={node.course.id} es la raíz.")

    def _node_grandparent(self):
        """
        Encuentra y muestra el nodo ABUELO del nodo seleccionado.
        El abuelo es simplemente el padre del padre.
        Se busca recursivamente: primero se encuentra el padre,
        y luego se busca el padre de ese padre.
        """        
        node = self._get_selected_node()
        if not node:
            return
        gp = self.tree.get_grandparent(node)
        if gp:
            self._log(f"Abuelo de ID={node.course.id}: ID={gp.course.id}")
            messagebox.showinfo(
                "Abuelo",
                f"Abuelo del nodo ID={node.course.id}:\n"
                f"ID={gp.course.id} | {gp.course.title[:50]}")
        else:
            messagebox.showinfo("Sin abuelo",
                                f"El nodo ID={node.course.id} no tiene abuelo.")

    def _node_uncle(self):
        """
        Encuentra y muestra el nodo TÍO del nodo seleccionado.
        El tío es el hermano del padre, es decir, el otro hijo del abuelo.
        Se busca recursivamente: se localiza el abuelo, y luego
        se retorna el hijo del abuelo que NO es el padre del nodo actual.
        """        
        node = self._get_selected_node()
        if not node:
            return
        uncle = self.tree.get_uncle(node)
        if uncle:
            self._log(f"Tío de ID={node.course.id}: ID={uncle.course.id}")
            messagebox.showinfo(
                "Tío",
                f"Tío del nodo ID={node.course.id}:\n"
                f"ID={uncle.course.id} | {uncle.course.title[:50]}")
        else:
            messagebox.showinfo("Sin tío",
                                f"El nodo ID={node.course.id} no tiene tío.")


# ──────────────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()