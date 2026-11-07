import tkinter as tk
from automata.fa.dfa import DFA

# 1. Definición matemática del DFA (El Cerebro)
dfa_foco = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    input_symbols={'e', 'a', 'b', 'r', 'v', 'z', 'p', 'i', 'g'},
    transitions={
        'q0':  {'e': 'q1'},
        'q1':  {'a': 'q0', 'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5', 'g': 'q9'},
        'q2':  {'a': 'q0', 'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'},
        'q3':  {'a': 'q0', 'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'},
        'q4':  {'a': 'q0', 'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'},
        'q5':  {'a': 'q0', 'b': 'q1', 'p': 'q10'},
        'q6':  {'a': 'q0', 'r': 'q2', 'p': 'q10'},
        'q7':  {'a': 'q0', 'v': 'q3', 'p': 'q10'},
        'q8':  {'a': 'q0', 'z': 'q4', 'p': 'q10'},
        'q9':  {'a': 'q0', 'p': 'q10'},
        'q10': {'a': 'q0', 'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'g': 'q9'}
    },
    initial_state='q0',
    final_states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    allow_partial=True  
)

# 2. Clase de la Máquina de Moore adaptada
class MaquinaDeMoore:
    def __init__(self, automata_dfa):
        self.motor_dfa = automata_dfa
        self.estado_actual = self.motor_dfa.initial_state

    def procesar_comando(self, simbolo):
        transiciones_disponibles = self.motor_dfa.transitions.get(self.estado_actual, {})
        if simbolo in transiciones_disponibles:
            self.estado_actual = transiciones_disponibles[simbolo]
            return True
        return False

# 3. Interfaz Gráfica Moderna con Tkinter
class SimuladorTiraLED:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Tira LED - Máquina de Moore")
        self.root.geometry("740x620")
        self.root.config(bg="#121214")

        self.maquina = MaquinaDeMoore(dfa_foco)
        self.animando_intermitente = False
        self.animando_rgb = False
        self.color_intermitente_activo = False
        self.rgb_offset = 0

        # Tarjeta contenedora principal estilo Web App
        main_frame = tk.Frame(root, bg="#18181b", bd=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título y subtítulo
        titulo = tk.Label(main_frame, text="💡 Simulador de Tira LED Inteligente", font=("Segoe UI", 18, "bold"), bg="#18181b", fg="#fafafa")
        titulo.pack(pady=(20, 5))

        sub = tk.Label(main_frame, text="Motor DFA + Máquina de Moore (Python Puro)", font=("Segoe UI", 10), bg="#18181b", fg="#a1a1aa")
        sub.pack(pady=(0, 15))

        # Panel visual de la Tira LED (Círculos con bordes limpios)
        self.frame_leds = tk.Frame(main_frame, bg="#121214", padx=15, pady=15)
        self.frame_leds.pack(pady=5)
        
        self.circulos_led = []
        for _ in range(6):
            c = tk.Canvas(self.frame_leds, width=72, height=72, bg="#121214", highlightthickness=0)
            circulo = c.create_oval(6, 6, 66, 66, fill="#27272a", outline="#3f3f46", width=3)
            c.pack(side=tk.LEFT, padx=8)
            self.circulos_led.append((c, circulo))

        # Etiqueta de estado físico actual (Salida de Moore)
        self.lbl_estado_fisico = tk.Label(main_frame, text="🔌 APAGADA", font=("Segoe UI", 13, "bold"), bg="#18181b", fg="#71717a")
        self.lbl_estado_fisico.pack(pady=15)

        # Panel de controles (Botones modernos)
        frame_controles = tk.Frame(main_frame, bg="#18181b")
        frame_controles.pack(pady=10, fill="x", padx=25)

        botones = [
            ('e', 'Encender (e)', '#10b981', '#059669'),
            ('a', 'Apagar (a)', '#ef4444', '#dc2626'),
            ('b', 'Blanco (b)', '#71717a', '#52525b'),
            ('r', 'Rojo (r)', '#f43f5e', '#e11d48'),
            ('v', 'Verde (v)', '#22c55e', '#16a34a'),
            ('z', 'Azul (z)', '#3b82f6', '#2563eb'),
            ('i', 'Intermitente (i)', '#f59e0b', '#d97706'),
            ('p', 'Patrones (p)', '#8b5cf6', '#7c3aed'),
            ('g', 'Arcoíris / RGB (g)', '#ec4899', '#db2777')
        ]

        for idx, (simbolo, texto, bg_color, active_color) in enumerate(botones):
            fila = idx // 3
            columna = idx % 3
            
            btn = tk.Button(
                frame_controles, text=texto, font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg="white", activebackground=active_color, activeforeground="white",
                relief="flat", cursor="hand2", width=18, height=2,
                command=lambda s=simbolo: self.ejecutar_comando(s)
            )
            btn.grid(row=fila, column=columna, padx=8, pady=6)
            frame_controles.grid_columnconfigure(columna, weight=1)

    def actualizar_interfaz_visual(self):
        estado = self.maquina.estado_actual
        self.animando_intermitente = False
        self.animando_rgb = False

        if estado == 'q0':
            self.cambiar_color_leds("#27272a")
            self.lbl_estado_fisico.config(text="🔌 APAGADA", fg="#71717a")
        elif estado == 'q1':
            self.cambiar_color_leds("#ffffff")
            self.lbl_estado_fisico.config(text="💡 BLANCA", fg="#ffffff")
        elif estado == 'q2':
            self.cambiar_color_leds("#f43f5e")
            self.lbl_estado_fisico.config(text="💡 ROJA", fg="#f43f5e")
        elif estado == 'q3':
            self.cambiar_color_leds("#22c55e")
            self.lbl_estado_fisico.config(text="💡 VERDE", fg="#22c55e")
        elif estado == 'q4':
            self.cambiar_color_leds("#3b82f6")
            self.lbl_estado_fisico.config(text="💡 AZUL", fg="#3b82f6")
        elif estado == 'q5':
            self.animando_intermitente = True
            self.lbl_estado_fisico.config(text="✨ BLANCA INTERMITENTE", fg="#ffffff")
            self.loop_intermitente("#ffffff")
        elif estado == 'q6':
            self.animando_intermitente = True
            self.lbl_estado_fisico.config(text="✨ ROJA INTERMITENTE", fg="#f43f5e")
            self.loop_intermitente("#f43f5e")
        elif estado == 'q7':
            self.animando_intermitente = True
            self.lbl_estado_fisico.config(text="✨ VERDE INTERMITENTE", fg="#22c55e")
            self.loop_intermitente("#22c55e")
        elif estado == 'q8':
            self.animando_intermitente = True
            self.lbl_estado_fisico.config(text="✨ AZUL INTERMITENTE", fg="#3b82f6")
            self.loop_intermitente("#3b82f6")
        elif estado == 'q9':
            self.animando_rgb = True
            self.lbl_estado_fisico.config(text="🌈 PATRÓN RGB / ARCOÍRIS", fg="#ec4899")
            self.rgb_offset = 0
            self.loop_rgb()
        elif estado == 'q10':
            self.cambiar_color_leds("#eab308")
            self.lbl_estado_fisico.config(text="⚙️ SELECTOR DE PATRÓN", fg="#eab308")

    def cambiar_color_leds(self, color_hex):
        for canvas, figura in self.circulos_led:
            canvas.itemconfig(figura, fill=color_hex, outline="#52525b")

    def loop_intermitente(self, color):
        if not self.animando_intermitente:
            return
        self.color_intermitente_activo = not self.color_intermitente_activo
        color_actual = color if self.color_intermitente_activo else "#18181b"
        self.cambiar_color_leds(color_actual)
        self.root.after(400, lambda: self.loop_intermitente(color))

    def loop_rgb(self):
        if not self.animando_rgb:
            return
        
        # Paleta de colores secuenciales para la tira LED
        colores = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6", "#8b5cf6", "#ec4899"]
        
        for idx, (canvas, figura) in enumerate(self.circulos_led):
            color_asignado = colores[(idx + self.rgb_offset) % len(colores)]
            canvas.itemconfig(figura, fill=color_asignado, outline="#ffffff")
            
        self.rgb_offset += 1
        self.root.after(300, self.loop_rgb)

    def ejecutar_comando(self, simbolo):
        exito = self.maquina.procesar_comando(simbolo)
        if exito:
            self.actualizar_interfaz_visual()
        else:
            self.lbl_estado_fisico.config(fg="#ef4444")
            self.root.after(300, lambda: self.actualizar_interfaz_visual())

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorTiraLED(root)
    root.mainloop()