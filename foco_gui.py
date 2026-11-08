"""
Simulador Gráfico Reactivo de Iluminación Inteligente (Máquina de Moore)
Materia: Fundamentos Teóricos de Informática (FTI)
"""

import tkinter as tk
from tkinter import ttk
import colorsys
import sys
from MaquinaDeMoore import MaquinaDeMoore
from luces import dfa_foco, salidas_foco

# Configuración de colores visuales por estado
COLORES_ESTADO = {
    'q0':  {'base': '#2b2b2b', 'glow': '#1f1f1f', 'texto': '#777777', 'nombre': 'Apagada'},
    'q1':  {'base': '#ffffff', 'glow': '#fff8db', 'texto': '#ffffff', 'nombre': 'Blanco'},
    'q2':  {'base': '#ff3b30', 'glow': '#ff6b6b', 'texto': '#ff3b30', 'nombre': 'Rojo'},
    'q3':  {'base': '#34c759', 'glow': '#69f0ae', 'texto': '#34c759', 'nombre': 'Verde'},
    'q4':  {'base': '#007aff', 'glow': '#70b5ff', 'texto': '#007aff', 'nombre': 'Azul'},
    'q5':  {'base': '#ffffff', 'glow': '#ffffff', 'texto': '#ffffff', 'nombre': 'Intermitente Blanco'},
    'q6':  {'base': '#ff3b30', 'glow': '#ff6b6b', 'texto': '#ff3b30', 'nombre': 'Intermitente Rojo'},
    'q7':  {'base': '#34c759', 'glow': '#69f0ae', 'texto': '#34c759', 'nombre': 'Intermitente Verde'},
    'q8':  {'base': '#007aff', 'glow': '#70b5ff', 'texto': '#007aff', 'nombre': 'Intermitente Azul'},
    'q9':  {'base': '#ff007f', 'glow': '#b388ff', 'texto': '#ff80bf', 'nombre': 'Patrón RGB'},
    'q10': {'base': '#ff9500', 'glow': '#ffd166', 'texto': '#ff9500', 'nombre': 'Selector de Patrón'}
}

COMANDOS_INFO = [
    ('e', 'Encender (e)', 'control'),
    ('a', 'Apagar (a)', 'control'),
    ('b', 'Blanco (b)', 'color'),
    ('r', 'Rojo (r)', 'color'),
    ('v', 'Verde (v)', 'color'),
    ('z', 'Azul (z)', 'color'),
    ('i', 'Intermitente (i)', 'efecto'),
    ('p', 'Menú Patrón (p)', 'efecto'),
    ('g', 'Modo RGB (g)', 'efecto'),
]

class FocoReactivoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Iluminación Inteligente - FTI")
        self.root.geometry("680x780")
        self.root.minsize(580, 720)
        self.root.configure(bg="#121316")

        # Instancia de la Máquina de Moore
        self.maquina = MaquinaDeMoore(dfa_foco, salidas_foco)
        self.palabra_formada = ""

        # Variables de animación
        self.parpadeo_activo = False
        self.parpadeo_fase = True
        self.rgb_hue = 0.0
        self.after_id = None

        self._crear_interfaz()
        self._vincular_teclado()
        self._actualizar_vista()
        self._loop_animacion()

    def _crear_interfaz(self):
        # 1. Encabezado
        header = tk.Frame(self.root, bg="#121316")
        header.pack(pady=(16, 8), padx=20, fill="x")

        tk.Label(
            header,
            text="💡 Foco Inteligente Reactivo",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#121316"
        ).pack()

        tk.Label(
            header,
            text="Control mediante Autómatas Finitos y Máquina de Moore",
            font=("Segoe UI", 10),
            fg="#8e9297",
            bg="#121316"
        ).pack(pady=(2, 0))

        # 2. Canvas del Foco
        self.canvas_size = 280
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#181a1f",
            highlightthickness=1,
            highlightbackground="#2b2f3a"
        )
        self.canvas.pack(pady=10)

        # 3. Panel de Estado Actual
        self.frame_estado = tk.Frame(self.root, bg="#181a1f", bd=1, relief="solid")
        self.frame_estado.configure(highlightbackground="#2b2f3a", highlightthickness=1)
        self.frame_estado.pack(padx=30, pady=8, fill="x")

        self.lbl_estado_nombre = tk.Label(
            self.frame_estado,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg="#181a1f",
            fg="#ffffff"
        )
        self.lbl_estado_nombre.pack(pady=(8, 2))

        self.lbl_estado_id = tk.Label(
            self.frame_estado,
            text="",
            font=("Consolas", 10),
            bg="#181a1f",
            fg="#8e9297"
        )
        self.lbl_estado_id.pack(pady=(0, 4))

        self.lbl_palabra = tk.Label(
            self.frame_estado,
            text="Palabra actual: (vacía)",
            font=("Consolas", 10),
            bg="#181a1f",
            fg="#61afef"
        )
        self.lbl_palabra.pack(pady=(0, 6))

        self.lbl_mensaje = tk.Label(
            self.frame_estado,
            text="Sistema iniciado. Ingrese un comando.",
            font=("Segoe UI", 10, "italic"),
            bg="#181a1f",
            fg="#98c379"
        )
        self.lbl_mensaje.pack(pady=(0, 8))

        # 4. Botonera reactiva
        frame_controles = tk.LabelFrame(
            self.root,
            text=" Comandos del Alfabeto (o pulsa la tecla correspondiente) ",
            font=("Segoe UI", 10, "bold"),
            bg="#121316",
            fg="#dcdfe4",
            padx=10,
            pady=10
        )
        frame_controles.pack(padx=24, pady=10, fill="both", expand=True)

        self.botones = {}
        # Distribución en cuadrícula 3x3
        for idx, (simbolo, etiqueta, tipo) in enumerate(COMANDOS_INFO):
            fila = idx // 3
            col = idx % 3

            color_btn = "#21252b"
            if tipo == "control":
                color_btn = "#2c313a"
            elif tipo == "color":
                color_btn = "#282c34"
            else:
                color_btn = "#21252b"

            btn = tk.Button(
                frame_controles,
                text=etiqueta,
                font=("Segoe UI", 10, "bold"),
                bg=color_btn,
                fg="#ffffff",
                activebackground="#3e4451",
                activeforeground="#61afef",
                relief="flat",
                bd=0,
                padx=8,
                pady=10,
                cursor="hand2",
                command=lambda s=simbolo: self.ejecutar_comando(s)
            )
            btn.grid(row=fila, column=col, padx=5, pady=5, sticky="nsew")
            self.botones[simbolo] = btn

        for c in range(3):
            frame_controles.columnconfigure(c, weight=1)
        for r in range(3):
            frame_controles.rowconfigure(r, weight=1)

        # 5. Barra inferior con botón de reset
        footer = tk.Frame(self.root, bg="#121316")
        footer.pack(fill="x", padx=24, pady=(0, 14))

        btn_reiniciar = tk.Button(
            footer,
            text="🔄 Reiniciar Sistema",
            font=("Segoe UI", 9),
            bg="#3e4451",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.reiniciar
        )
        btn_reiniciar.pack(side="left")

        tk.Label(
            footer,
            text="Presioná teclas: e, a, b, r, v, z, p, i, g",
            font=("Segoe UI", 9),
            fg="#5c6370",
            bg="#121316"
        ).pack(side="right")

    def _vincular_teclado(self):
        # Escucha teclas en toda la ventana
        self.root.bind("<Key>", self._al_pulsar_tecla)

    def _al_pulsar_tecla(self, event):
        tecla = event.char.lower()
        if tecla in dfa_foco.input_symbols:
            self.ejecutar_comando(tecla)

    def ejecutar_comando(self, simbolo):
        estado_previo = self.maquina.estado_actual
        fue_aceptado, salida = self.maquina.procesar_comando(simbolo)

        if fue_aceptado:
            self.palabra_formada += simbolo
            self.lbl_mensaje.config(
                text=f"✅ Comando '{simbolo}': Transición {estado_previo} ➔ {self.maquina.estado_actual}",
                fg="#98c379"
            )
        else:
            self.lbl_mensaje.config(
                text=f"❌ Comando '{simbolo}' rechazado desde el estado {estado_previo}",
                fg="#e06c75"
            )

        self._actualizar_vista()

    def reiniciar(self):
        self.maquina.estado_actual = dfa_foco.initial_state
        self.palabra_formada = ""
        self.lbl_mensaje.config(
            text="Sistema reiniciado al estado inicial.",
            fg="#61afef"
        )
        self._actualizar_vista()

    def _actualizar_vista(self):
        estado = self.maquina.estado_actual
        info_color = COLORES_ESTADO.get(estado, COLORES_ESTADO['q0'])

        # Actualiza etiquetas informativas
        salida_texto = self.maquina.obtener_estado_fisico()
        self.lbl_estado_nombre.config(text=salida_texto, fg=info_color['texto'])
        self.lbl_estado_id.config(text=f"Estado Matemático: [{estado}]")
        self.lbl_palabra.config(
            text=f"Cadena formada: '{self.palabra_formada}' (longitud: {len(self.palabra_formada)})"
        )

        # Destaca botones disponibles para el estado actual
        transiciones_disponibles = dfa_foco.transitions.get(estado, {})
        for s, btn in self.botones.items():
            if s in transiciones_disponibles:
                btn.config(
                    bg="#2d3748",
                    fg="#63b3ed",
                    relief="solid",
                    bd=1,
                    highlightbackground="#4299e1"
                )
            else:
                btn.config(
                    bg="#1a202c",
                    fg="#4a5568",
                    relief="flat",
                    bd=0
                )

        # Redibuja el foco
        self._dibujar_foco()

    def _dibujar_foco(self):
        self.canvas.delete("all")
        cx = self.canvas_size / 2
        cy = self.canvas_size / 2 - 15

        estado = self.maquina.estado_actual
        info = COLORES_ESTADO.get(estado, COLORES_ESTADO['q0'])

        # Si está apagada (q0)
        if estado == 'q0':
            color_cuerpo = "#333742"
            color_brillo = "#22252c"
            radio_cuerpo = 55
            # Sin halo
        elif estado in ('q5', 'q6', 'q7', 'q8'):
            # Intermitente: alterna en la animación
            if self.parpadeo_fase:
                color_cuerpo = info['base']
                color_brillo = info['glow']
            else:
                color_cuerpo = "#424754"
                color_brillo = "#2b2f3a"
            radio_cuerpo = 55
        elif estado == 'q9':
            # RGB Dinámico
            rgb = colorsys.hsv_to_rgb(self.rgb_hue, 0.85, 1.0)
            color_cuerpo = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
            color_brillo = color_cuerpo
            radio_cuerpo = 55
        else:
            color_cuerpo = info['base']
            color_brillo = info['glow']
            radio_cuerpo = 55

        # 1. Halos de resplandor exterior si está encendida
        if estado != 'q0' and (estado not in ('q5', 'q6', 'q7', 'q8') or self.parpadeo_fase):
            for r, alpha_color in [(110, "#1f2530"), (90, "#232d3b"), (75, color_brillo)]:
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill=alpha_color if r != 75 else color_brillo,
                    outline="",
                    stipple="gray50" if r != 75 else ""
                )

        # 2. Rayos de luz / destellos para modos intermitentes o encendidos
        if estado != 'q0' and (estado not in ('q5', 'q6', 'q7', 'q8') or self.parpadeo_fase):
            import math
            rayos = 8
            for i in range(rayos):
                angulo = i * (2 * math.pi / rayos)
                x1 = cx + math.cos(angulo) * 65
                y1 = cy + math.sin(angulo) * 65
                x2 = cx + math.cos(angulo) * 82
                y2 = cy + math.sin(angulo) * 82
                self.canvas.create_line(x1, y1, x2, y2, fill=color_brillo, width=3, capstyle="round")

        # 3. Base de casquillo (rosca metálica inferior)
        self.canvas.create_rectangle(cx - 20, cy + 50, cx + 20, cy + 85, fill="#4a4f5d", outline="#2b2f3a")
        for h in (56, 64, 72, 80):
            self.canvas.create_line(cx - 18, cy + h, cx + 18, cy + h, fill="#717888", width=2)
        # Contacto inferior redondeado
        self.canvas.create_arc(cx - 12, cy + 80, cx + 12, cy + 92, start=180, extent=180, fill="#2b2f3a", outline="")

        # 4. Cuerpo de cristal del foco (bulbo)
        # Forma combinada: círculo superior y trapecio hacia el casquillo
        self.canvas.create_polygon(
            cx - 40, cy + 15,
            cx - 20, cy + 52,
            cx + 20, cy + 52,
            cx + 40, cy + 15,
            fill=color_cuerpo,
            outline="#22252c",
            width=2
        )
        self.canvas.create_oval(
            cx - radio_cuerpo, cy - radio_cuerpo,
            cx + radio_cuerpo, cy + radio_cuerpo,
            fill=color_cuerpo,
            outline="#22252c",
            width=2
        )

        # 5. Filamento / Reflejo interior
        if estado == 'q0':
            # Filamento apagado visible
            self.canvas.create_line(cx - 14, cy + 20, cx - 7, cy - 8, fill="#5c6370", width=2)
            self.canvas.create_line(cx + 14, cy + 20, cx + 7, cy - 8, fill="#5c6370", width=2)
            self.canvas.create_arc(cx - 8, cy - 18, cx + 8, cy - 2, start=0, extent=180, style="arc", outline="#5c6370", width=2)
        else:
            # Reflejo brillante de cristal
            self.canvas.create_arc(
                cx - 44, cy - 44, cx + 44, cy + 44,
                start=110, extent=65, style="arc",
                outline="#ffffff", width=4
            )

    def _loop_animacion(self):
        """Bucle para efectos animados (intermitencia y arcoíris RGB)."""
        estado = self.maquina.estado_actual
        redibujar = False

        # Modo Intermitente
        if estado in ('q5', 'q6', 'q7', 'q8'):
            self.parpadeo_fase = not self.parpadeo_fase
            redibujar = True

        # Modo RGB
        if estado == 'q9':
            self.rgb_hue = (self.rgb_hue + 0.05) % 1.0
            redibujar = True

        if redibujar:
            self._dibujar_foco()

        # Programa el siguiente frame
        delay_ms = 400 if estado in ('q5', 'q6', 'q7', 'q8') else 100
        self.after_id = self.root.after(delay_ms, self._loop_animacion)


def main():
    root = tk.Tk()
    app = FocoReactivoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
