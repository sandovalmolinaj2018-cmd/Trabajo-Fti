import tkinter as tk

class VistaTiraLed:
    def __init__(self, root):
        self.root = root
        self.controlador = None
        self.root.title("Simulador de Tira LED")
        self.root.geometry("760x560")
        self.root.minsize(640, 420)
        self.root.configure(bg="#222222")


        self.main_canvas = tk.Canvas(self.root, bg="#222222", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#222222")
        self.canvas_window = self.main_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )


        self.scrollable_frame.bind("<Configure>", self.ajustar_scroll)
        self.main_canvas.bind("<Configure>", self.ajustar_ancho)


        self.main_canvas.bind("<MouseWheel>", self.mover_scroll)
        self.main_canvas.bind("<Button-4>", self.mover_scroll)
        self.main_canvas.bind("<Button-5>", self.mover_scroll)
        self.root.bind_all("<MouseWheel>", self.mover_scroll)
        self.root.bind_all("<Button-4>", self.mover_scroll)
        self.root.bind_all("<Button-5>", self.mover_scroll)

        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Focos
        self.frame_focos = tk.Frame(self.scrollable_frame, bg="#222222")
        self.frame_focos.pack(pady=14)
        self.focos_canvas = []

        # Botones
        self.botones = {}
        self.botones_colores = []
        self.botones_brillo = []
        self.crear_botones()

    def ajustar_scroll(self, event=None):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def ajustar_ancho(self, event):
        req_w = self.scrollable_frame.winfo_reqwidth()
        new_w = max(event.width, req_w)
        self.main_canvas.itemconfig(self.canvas_window, width=new_w)

    def mover_scroll(self, event):
        if event.num == 4:
            self.main_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.main_canvas.yview_scroll(1, "units")
        elif hasattr(event, "delta") and event.delta:
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def poner_controlador(self, controlador):
        self.controlador = controlador

    def programar(self, ms, callback):
        self.root.after(ms, callback)

    def crear_botones(self):
        # panel de colores y modos
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

        # fila 1: encender, apagar, blanco
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
                command=lambda c=comando: self.mandar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # fila 2: rojo, verde, azul
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
                command=lambda c=comando: self.mandar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # fila 3: intermitente, patrones, RGB
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
                command=lambda c=comando: self.mandar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_colores.append(btn)

        # panel de brillo
        self.frame_brillo = tk.LabelFrame(
            self.scrollable_frame,
            text=" Nivel de Brillo ",
            bg="#222222",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=6,
            pady=4,
            relief="groove"
        )
        self.frame_brillo.pack(pady=4, padx=6, fill="x")

        # botones de brillo
        self.frame_brillo_fila = tk.Frame(self.frame_brillo, bg="#222222")
        self.frame_brillo_fila.pack(pady=2)

        brillos = [
            ('1', '1: Muy bajo'),
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
                command=lambda c=comando: self.mandar_comando(c)
            )
            btn.pack(side="left", padx=2)
            self.botones[comando] = btn
            self.botones_brillo.append(btn)

    def mandar_comando(self, comando):
        # le pasa al controlador el botón apretado
        if self.controlador:
            self.controlador.recibir_comando(comando)

    def dibujar_focos(self, cantidad):
        for _ in range(cantidad):
            c = tk.Canvas(self.frame_focos, width=60, height=60, bg="#222222", highlightthickness=0)
            c.pack(side="left", padx=5)
            
            # Foco
            foco = c.create_oval(5, 5, 55, 55, fill="black", outline="gray", width=2)
            
            # sombra
            sombra = c.create_oval(5, 5, 55, 55, fill="", outline="")
            
            self.focos_canvas.append((c, foco, sombra))

    def pintar_focos(self, colores_tira, estado_brillo):

        # cuánto se atenúa el color según el brillo
        factores = {
            "Muy bajo": 0.2,
            "Bajo": 0.4,
            "Medio": 0.6,
            "Alto": 0.8,
            "Máximo": 1.0,
        }
        factor = factores.get(estado_brillo, 1.0)
        
        for i in range(len(self.focos_canvas)):
            canvas, foco, sombra = self.focos_canvas[i]

            r, g, b = self.root.winfo_rgb(colores_tira[i])
            r = int(r / 256 * factor)
            g = int(g / 256 * factor)
            b = int(b / 256 * factor)

            color_final = f"#{r:02x}{g:02x}{b:02x}"
            canvas.itemconfig(foco, fill=color_final)