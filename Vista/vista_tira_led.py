import tkinter as tk

class VistaTiraLed:
    def __init__(self, root):
        self.root = root
        self.controlador = None
        self.root.title("Simulador de Tira LED")
        self.root.geometry("800x400")
        self.root.configure(bg="#222222")

        # 1. ZONA SUPERIOR: Contenedor para los círculos de la tira LED
        self.frame_focos = tk.Frame(self.root, bg="#222222")
        self.frame_focos.pack(pady=50)
        self.focos_canvas = []  # Acá guardaremos los círculos dibujados

        # 2. ZONA INFERIOR: Contenedores para los botones
        tk.Label(self.root, text="Controles de Color:", bg="#222222", fg="white").pack()
        self.frame_colores = tk.Frame(self.root, bg="#222222")
        self.frame_colores.pack(pady=5)

        tk.Label(self.root, text="Controles de Brillo:", bg="#222222", fg="white").pack(pady=(15, 0))
        self.frame_brillo = tk.Frame(self.root, bg="#222222")
        self.frame_brillo.pack(pady=5)

        self._crear_botones()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def _crear_botones(self):
        # Botones del autómata de Color
        colores = [
            ('e', 'Encender', 'gray'), ('a', 'Apagar', 'black'),
            ('b', 'Blanco', 'white'), ('r', 'Rojo', 'red'),
            ('v', 'Verde', 'green'), ('z', 'Azul', 'blue'),
            ('i', 'Intermitente', 'orange'), ('p', 'Patrones', 'purple'),
            ('g', 'RGB', 'magenta')
        ]
        
        for comando, texto, color_bg in colores:
            # Color de letra negro si el fondo es blanco/gris, sino blanco
            color_fg = "black" if color_bg in ["white", "gray"] else "white"
            btn = tk.Button(self.frame_colores, text=texto, bg=color_bg, fg=color_fg, width=10,
                            command=lambda c=comando: self.enviar_comando(c))
            btn.pack(side="left", padx=3)

        # Botones del autómata de Brillo
        brillos = [
            ('1', 'Bajo (1)'), ('2', 'Tenue (2)'), ('3', 'Medio (3)'),
            ('4', 'Alto (4)'), ('5', 'Máximo (5)')
        ]
        
        for comando, texto in brillos:
            btn = tk.Button(self.frame_brillo, text=texto, bg="#444444", fg="white", width=10,
                            command=lambda c=comando: self.enviar_comando(c))
            btn.pack(side="left", padx=5)

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
            "Bajo": 0.2,
            "Tenue": 0.4,
            "Medio": 0.6,
            "Alto": 0.8,
            "Maximo": 1.0
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
