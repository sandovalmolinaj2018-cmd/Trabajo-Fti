from Modelo.foco import Foco
from Modelo.brillo import Brillo

class ControladorTiraLed:
    def __init__(self, vista):
        self.vista = vista
        self.vista.poner_controlador(self)

        # Tira led
        self.cantidad_focos = 5
        self.tira_focos = []
        for i in range(self.cantidad_focos):
            self.tira_focos.append(Foco(verbose=(i == 0)))

        self.control_brillo = Brillo()

        # datos para la animación
        self.fase = 0
        self.intervalo_ms = 500
        self.secuencia_rgb = ["red", "green", "blue"]

        
        self.colores_tk = {
            "Apagado": "black",
            "Blanco": "white",
            "Rojo": "red",
            "Verde": "green",
            "Azul": "blue",
            "Intermitente blanco": "white",
            "Intermitente rojo": "red",
            "Intermitente verde": "green",
            "Intermitente azul": "blue",
            "Menu Patrones": "yellow"
        }

    def iniciar(self):
        self.vista.dibujar_focos(self.cantidad_focos)
        self.refrescar()
        self.vista.programar(self.intervalo_ms, self.animar)

    def animar(self):
        self.fase += 1
        self.refrescar()
        self.vista.programar(self.intervalo_ms, self.animar)

    def recibir_comando(self, comando):
        numeros_brillo = ['1', '2', '3', '4', '5']

        if comando in numeros_brillo:
            self.control_brillo.procesar_entrada(comando)

        elif comando == 'd':
            for foco in self.tira_focos:
                foco.retroceder()

        else:
            transicion_valida = False
            for foco in self.tira_focos:
                res = foco.procesar_entrada(comando)
                if res is not None:
                    transicion_valida = True
            if transicion_valida:
                self.fase = 0  # reinicia el parpadeo / RGB

        self.refrescar()

    def refrescar(self):
        colores_para_pintar = []

        for i, foco in enumerate(self.tira_focos):
            estado_texto = foco.obtener_estado_actual()
            color_foco = self.colores_tk.get(estado_texto, "black")

            if estado_texto.startswith("Intermitente"):
                # Si es par prende, sino se apaga
                if self.fase % 2 == 1:
                    color_foco = "black"

            elif estado_texto == "Patron RGB":
                # Genera el efecto de ola
                color_foco = self.secuencia_rgb[(self.fase + i) % len(self.secuencia_rgb)]

            colores_para_pintar.append(color_foco)

        estado_brillo = self.control_brillo.obtener_estado_actual()
        self.vista.pintar_focos(colores_para_pintar, estado_brillo)