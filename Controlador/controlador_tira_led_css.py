from Modelo.foco import Foco
from Modelo.brillo import Brillo

class ControladorTiraLedCss:
    def __init__(self):
        # Creacion tira led
        self.cantidad_focos = 5
        self.tira_focos = []
        for i in range(self.cantidad_focos):
            self.tira_focos.append(Foco(verbose=(i == 0)))

        self.control_brillo = Brillo()

        # Animación (intermitente y RGB)
        self.fase = 0
        self.intervalo_ms = 500
        self.secuencia_rgb = ["red", "green", "blue"]

        # Variables para almacenar el último estado y entregárselo a la web
        self.colores_ultimos = ["black"] * self.cantidad_focos
        self.brillo_actual = "Maximo"

        # Traduccion entre el modelo y la vista web
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
            "Patron RGB": "magenta",   # no se usa, el RGB se calcula con la fase
            "Menu Patrones": "yellow"
        }

    def procesar_comando(self, comando):
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
                self.fase = 0  # el parpadeo / RGB arranca siempre desde el principio

        self.actualizar_pantalla()

    def avanzar_animacion(self):
        # Llamado periódicamente por el hilo en segundo plano para las animaciones
        self.fase += 1
        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        colores_para_pintar = []

        for i, foco in enumerate(self.tira_focos):
            estado_texto = foco.obtener_estado_actual()
            color_foco = self.colores_tk.get(estado_texto, "black")

            if estado_texto.startswith("Intermitente"):
                # Fase par: prendido, fase impar: apagado
                if self.fase % 2 == 1:
                    color_foco = "black"

            elif estado_texto == "Patron RGB":
                # Cada foco va desfasado uno del otro, queda efecto "ola"
                color_foco = self.secuencia_rgb[(self.fase + i) % len(self.secuencia_rgb)]

            colores_para_pintar.append(color_foco)

        self.brillo_actual = self.control_brillo.obtener_estado_actual()
        self.colores_ultimos = colores_para_pintar