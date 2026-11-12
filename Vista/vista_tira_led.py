import tkinter as tk

class VistaTiraLed:
    def __init__(self, root):
        self.root = root
        self.controlador = None
        self.root.title("Simulador de Tira LED")
        self.root.geometry("760x560")
        self.root.minsize(640, 420)
        self.root.configure(bg="#222222")

        # Contenedor desplazable (Canvas + Scrollbar vertical) para garantizar
        # que todos los controles permanezcan visibles y accesibles en cualquier resolución.
        self.main_canvas = tk.Canvas(self.root, bg="#222222", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#222222")
        self.canvas_window = self.main_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Enlace de eventos dinámicos para adaptación de scroll
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.main_canvas.bind("<Configure>", self._on_canvas_configure)

        # Enlace de eventos de scroll con rueda de ratón (multiplataforma)
        self.main_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.main_canvas.bind("<Button-4>", self._on_mousewheel)
        self.main_canvas.bind("<Button-5>", self._on_mousewheel)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # 1. ZONA SUPERIOR: Contenedor para los círculos de la tira LED (padding reducido a 14)
        self.frame_focos = tk.Frame(self.scrollable_frame, bg="#222222")
        self.frame_focos.pack(pady=14)
        self.focos_canvas = []  # Círculos dibujados

        # 2. ZONA DE CONTROLES: Agrupación ergonómica
        self.botones = {}
        self.botones_colores = []
        self.botones_brillo = []
        self.boton_deshacer = None
        self.botones_presets_cargar = {}
        self.botones_presets_guardar = {}
        self._crear_botones()

    def _on_frame_configure(self, event=None):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        req_w = self.scrollable_frame.winfo_reqwidth()
        new_w = max(event.width, req_w)
        self.main_canvas.itemconfig(self.canvas_window, width=new_w)

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.main_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.main_canvas.yview_scroll(1, "units")
        elif hasattr(event, "delta") and event.delta:
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_controlador(self, controlador):
        self.controlador = controlador

    def programar(self, ms, callback):
        # Le permite al controlador pedir "llamame de nuevo en X ms"
        self.root.after(ms, callback)

    def _crear_botones(self):
        # Panel Controles de Color y Modos: agrupado en 3 filas equilibradas (<= 550px reqwidth)
        self.frame_colores = tk.LabelFrame(
            self.scrollable_frame,
            text=" Controles de Color y Modos ",
            bg="#222222",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=6,
            pady=4,
            relief="groove"
        )
        self.frame_colores.pack(pady=4, padx=6, fill="x")

        # Fila 1 (Encender, Apagar, Blanco): 3 botones
        self.frame_colores_r1 = tk.Frame(self.frame_colores, bg="#222222")
        self.frame_colores_r1.pack(pady=2)

        colores_r1 = [
            ('e', 'Encender (e)', '#4b5563', 'white', 13),
            ('a', 'Apagar (a)', '#18181b', 'white', 13),
            ('b', 'Blanco (b)', '#f3f4f6', 'black', 13),
        ]

        for comando, texto, bg, fg, width in colores_r1:
            btn = tk.Button(
                self.frame_colores_r1,
                text=texto,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                width=width,
                relief="raised",
                cursor="hand2",
                command=lambda c=comando: self.enviar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # Fila 2 (Rojo, Verde, Azul): 3 botones
        self.frame_colores_r2 = tk.Frame(self.frame_colores, bg="#222222")
        self.frame_colores_r2.pack(pady=2)

        colores_r2 = [
            ('r', 'Rojo (r)', '#dc2626', 'white', 13),
            ('v', 'Verde (v)', '#16a34a', 'white', 13),
            ('z', 'Azul (z)', '#2563eb', 'white', 13),
        ]

        for comando, texto, bg, fg, width in colores_r2:
            btn = tk.Button(
                self.frame_colores_r2,
                text=texto,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                width=width,
                relief="raised",
                cursor="hand2",
                command=lambda c=comando: self.enviar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # Fila 3 (Animaciones y Patrones): Intermitente (i), Patrones (p), RGB / Arcoíris (g)
        self.frame_colores_r3 = tk.Frame(self.frame_colores, bg="#222222")
        self.frame_colores_r3.pack(pady=2)

        colores_r3 = [
            ('i', 'Intermitente (i)', '#d97706', 'white', 15),
            ('p', 'Patrones (p)', '#7c3aed', 'white', 15),
            ('g', 'RGB / Arcoíris (g)', '#db2777', 'white', 17),
        ]

        for comando, texto, bg, fg, width in colores_r3:
            btn = tk.Button(
                self.frame_colores_r3,
                text=texto,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                width=width,
                relief="raised",
                cursor="hand2",
                command=lambda c=comando: self.enviar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # Panel Nivel de Brillo e Historial: 2 filas compactas
        self.frame_brillo = tk.LabelFrame(
            self.scrollable_frame,
            text=" Nivel de Brillo e Historial ",
            bg="#222222",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=6,
            pady=4,
            relief="groove"
        )
        self.frame_brillo.pack(pady=4, padx=6, fill="x")

        # Fila 1: 5 niveles de brillo (1 a 5)
        self.frame_brillo_fila = tk.Frame(self.frame_brillo, bg="#222222")
        self.frame_brillo_fila.pack(pady=2)

        brillos = [
            ('1', '1: Muy Bajo'),
            ('2', '2: Bajo'),
            ('3', '3: Medio'),
            ('4', '4: Alto'),
            ('5', '5: Máximo'),
        ]

        for comando, texto in brillos:
            btn = tk.Button(
                self.frame_brillo_fila,
                text=texto,
                bg="#374151",
                fg="white",
                activebackground="#4b5563",
                activeforeground="white",
                width=8,
                relief="raised",
                cursor="hand2",
                command=lambda c=comando: self.enviar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_brillo.append(btn)

        # Fila 2: Botón de historial (autómata de pila): Deshacer (d) destacado
        self.frame_historial = tk.Frame(self.frame_brillo, bg="#222222")
        self.frame_historial.pack(pady=2)

        self.boton_deshacer = tk.Button(
            self.frame_historial,
            text="↶ Deshacer (d)",
            bg="#9a3412",
            fg="white",
            activebackground="#c2410c",
            activeforeground="white",
            width=18,
            relief="raised",
            cursor="hand2",
            command=lambda: self.enviar_comando('d')
        )
        self.boton_deshacer.pack(side="left", padx=2)
        self.botones['d'] = self.boton_deshacer

        # Panel Presets de Iluminación: 3 slots para guardar y restaurar estados
        self.frame_presets = tk.LabelFrame(
            self.scrollable_frame,
            text=" Presets de Iluminación ",
            bg="#222222",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=6,
            pady=4,
            relief="groove"
        )
        self.frame_presets.pack(pady=4, padx=6, fill="x")

        for slot in (1, 2, 3):
            frame_slot = tk.Frame(self.frame_presets, bg="#222222")
            frame_slot.pack(pady=2)

            lbl = tk.Label(
                frame_slot,
                text=f"Slot {slot}:",
                bg="#222222",
                fg="white",
                font=("Arial", 9, "bold"),
                width=7,
                anchor="w"
            )
            lbl.pack(side="left", padx=3)

            btn_cargar = tk.Button(
                frame_slot,
                text=f"⚡ P{slot}: Vacío",
                bg="#374151",
                fg="white",
                activebackground="#4b5563",
                activeforeground="white",
                width=28,
                relief="raised",
                cursor="hand2",
                command=lambda s=slot: self.cargar_preset(s)
            )
            btn_cargar.pack(side="left", padx=3)
            self.botones_presets_cargar[slot] = btn_cargar

            btn_guardar = tk.Button(
                frame_slot,
                text="💾 Guardar",
                bg="#047857",
                fg="white",
                activebackground="#059669",
                activeforeground="white",
                width=10,
                relief="raised",
                cursor="hand2",
                command=lambda s=slot: self.guardar_preset(s)
            )
            btn_guardar.pack(side="left", padx=3)
            self.botones_presets_guardar[slot] = btn_guardar

        # Etiqueta de retroalimentación para acciones de presets
        self.lbl_mensaje_presets = tk.Label(
            self.frame_presets,
            text="",
            bg="#222222",
            fg="#f87171",
            font=("Arial", 9, "italic")
        )
        self.lbl_mensaje_presets.pack(pady=2)


    def enviar_comando(self, comando):
        # Le avisa al controlador qué botón se apretó
        if self.controlador:
            self.controlador.procesar_comando(comando)

    def dibujar_tira(self, cantidad):
        for _ in range(cantidad):
            c = tk.Canvas(self.frame_focos, width=60, height=60, bg="#222222", highlightthickness=0)
            c.pack(side="left", padx=5)
            
            # foco de color
            foco = c.create_oval(5, 5, 55, 55, fill="black", outline="gray", width=2)
            
            # Sombra foco
            sombra = c.create_oval(5, 5, 55, 55, fill="", outline="")
            
            self.focos_canvas.append((c, foco, sombra))

    def actualizar_luces(self, colores_tira, estado_brillo):
        # Factor de intensidad según el estado del autómata de brillo
        factores = {
            "Muy Bajo": 0.2,
            "Bajo": 0.4,
            "Medio": 0.6,
            "Alto": 0.8,
            "Maximo": 1.0,
        }
        factor = factores.get(estado_brillo, 1.0)
        
        for i in range(len(self.focos_canvas)):
            canvas, foco, sombra = self.focos_canvas[i]

            # winfo_rgb convierte cualquier color de Tk ("red", "#ff0000", etc.)
            # a valores de 0 a 65535, por eso se divide por 256
            r, g, b = self.root.winfo_rgb(colores_tira[i])
            r = int(r / 256 * factor)
            g = int(g / 256 * factor)
            b = int(b / 256 * factor)

            color_final = f"#{r:02x}{g:02x}{b:02x}"
            canvas.itemconfig(foco, fill=color_final)

    def cargar_preset(self, slot):
        if self.controlador:
            self.controlador.cargar_preset(slot)

    def guardar_preset(self, slot):
        if self.controlador:
            self.controlador.guardar_preset(slot)

    def actualizar_texto_preset(self, slot, texto):
        try:
            slot_num = int(slot)
        except (ValueError, TypeError):
            slot_num = slot

        try:
            if slot_num in self.botones_presets_cargar:
                self.botones_presets_cargar[slot_num].configure(text=texto)
        except TypeError:
            pass

    def mostrar_mensaje_preset(self, texto, es_error=True):
        try:
            if hasattr(self, 'lbl_mensaje_presets') and self.lbl_mensaje_presets:
                color = "#f87171" if es_error else "#34d399"
                self.lbl_mensaje_presets.configure(text=texto, fg=color)
                if hasattr(self, 'root') and self.root:
                    self.root.after(4000, lambda: self.lbl_mensaje_presets.configure(text="") if hasattr(self, 'lbl_mensaje_presets') else None)
        except Exception:
            pass

