from Modelo.foco import Foco
from Modelo.brillo import Brillo
from Modelo.presets import MemoriaPresets


class ControladorTiraLed:
    def __init__(self, vista):
        self.vista = vista
        self.vista.poner_controlador(self)

        # Tira led de 5 focos
        self.cantidad_focos = 5
        self.tira_focos = []
        for i in range(self.cantidad_focos):
            if i == 0:
                mostrar = True
            else:
                mostrar = False
            self.tira_focos.append(Foco(mostrar_mensajes=mostrar))

        self.control_brillo = Brillo(mostrar_mensajes=True)
        self.memoria_all = MemoriaPresets(mostrar_mensajes=True)

        # Datos para la animacion
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
            "Patron RGB": "magenta",
            "Menu Patrones": "yellow"
        }

        self.mapa_estado_a_cadena_w = {
            'q1': 'e',
            'q2': 'er',
            'q3': 'ev',
            'q4': 'ez',
            'q5': 'ei',
            'q6': 'eri',
            'q7': 'evi',
            'q8': 'ezi',
            'q9': 'eg',
            'q10': 'ep'
        }

        self.mapa_brillo_a_comando = {
            'q0': '1',
            'q1': '2',
            'q2': '3',
            'q3': '4',
            'q4': '5'
        }

    def iniciar(self):
        self.vista.dibujar_focos(self.cantidad_focos)
        self.sincronizar_botones_presets()
        self.refrescar()
        self.vista.programar(self.intervalo_ms, self.animar)

    def animar(self):
        self.fase = self.fase + 1
        self.refrescar()
        self.vista.programar(self.intervalo_ms, self.animar)

    def recibir_comando(self, comando):
        numeros_brillo = ['1', '2', '3', '4', '5']

        if comando in numeros_brillo:
            self.control_brillo.transicionar(comando)

        elif comando == 'e' and self.tira_focos[0].obtener_estado_actual() == 'q0':
            tope_pila = self.tira_focos[0].obtener_tope()
            if tope_pila == 'Z':
                datos_defecto = self.memoria_all.leer_desde_slot('DEF')
                if datos_defecto is not None:
                    self.consumir_preset_en_dpda(datos_defecto)
                else:
                    for foco in self.tira_focos:
                        foco.procesar_entrada('e')
            else:
                for foco in self.tira_focos:
                    foco.procesar_entrada('e')
            self.fase = 0

        elif comando == 'd':
            for foco in self.tira_focos:
                foco.retroceder()

        else:
            transicion_valida = False
            for foco in self.tira_focos:
                res = foco.procesar_entrada(comando)
                if res is not None:
                    transicion_valida = True

            if transicion_valida == True:
                self.fase = 0

        self.refrescar()

    def consumir_preset_en_dpda(self, datos_preset):
        cadena_w = datos_preset["cadena_w"]
        comando_brillo = datos_preset["comando_brillo"]

        for i in range(len(self.tira_focos)):
            foco = self.tira_focos[i]
            foco.reiniciar_pila()

            for simbolo in cadena_w:
                if i == 0:
                    foco.procesar_entrada(simbolo, mostrar_mensaje_terminal=True)
                else:
                    foco.procesar_entrada(simbolo, mostrar_mensaje_terminal=False)

        self.control_brillo.transicionar(comando_brillo)

    def guardar_preset(self, identificador_slot):
        estado_foco = self.tira_focos[0].obtener_estado_actual()

        if estado_foco == 'q0':
            self.vista.mostrar_mensaje_preset("No se puede guardar con la tira apagada", es_error=True)
            return False

        estado_brillo = self.control_brillo.estado_actual
        nombre_color = self.tira_focos[0].obtener_salida_actual()
        nombre_brillo = self.control_brillo.obtener_salida()

        if estado_foco in self.mapa_estado_a_cadena_w:
            cadena_w = self.mapa_estado_a_cadena_w[estado_foco]
        else:
            cadena_w = "e"

        if estado_brillo in self.mapa_brillo_a_comando:
            comando_brillo = self.mapa_brillo_a_comando[estado_brillo]
        else:
            comando_brillo = "5"

        datos_preset = {
            "cadena_w": cadena_w,
            "comando_brillo": comando_brillo,
            "estado_foco": estado_foco,
            "estado_brillo": estado_brillo,
            "nombre_color": nombre_color,
            "nombre_brillo": nombre_brillo
        }

        exito = self.memoria_all.escribir_en_slot(identificador_slot, datos_preset)
        if exito == True:
            self.sincronizar_botones_presets()
            self.refrescar()
            self.vista.mostrar_mensaje_preset("Preset " + str(identificador_slot) + " guardado: " + str(nombre_color), es_error=False)
            return True
        else:
            return False

    def cargar_preset(self, identificador_slot):
        if self.tira_focos[0].obtener_estado_actual() == 'q0':
            self.vista.mostrar_mensaje_preset("Enciende la tira antes de cargar un preset", es_error=True)
            return False

        datos_preset = self.memoria_all.leer_desde_slot(identificador_slot)
        if datos_preset is None:
            self.vista.mostrar_mensaje_preset("El slot " + str(identificador_slot) + " esta vacio", es_error=True)
            return False

        self.consumir_preset_en_dpda(datos_preset)
        self.fase = 0
        self.refrescar()
        self.vista.mostrar_mensaje_preset("Preset " + str(identificador_slot) + " cargado", es_error=False)
        return True

    def sincronizar_botones_presets(self):
        slots_disponibles = ['DEF', 1, 2, 3]

        for slot in slots_disponibles:
            indice_celda = self.memoria_all.mapa_slots[slot]
            datos = self.memoria_all.cinta[indice_celda]

            if slot == 'DEF':
                prefijo = "DEF"
            else:
                prefijo = "P" + str(slot)

            if datos is not None:
                texto = prefijo + ": " + str(datos["nombre_color"]) + " (" + str(datos["nombre_brillo"]) + ")"
            else:
                texto = prefijo + ": Vacio"

            self.vista.actualizar_texto_preset(slot, texto)

    def refrescar(self):
        colores_para_pintar = []

        for i in range(len(self.tira_focos)):
            foco = self.tira_focos[i]
            estado_texto = foco.obtener_salida_actual()

            if estado_texto in self.colores_tk:
                color_foco = self.colores_tk[estado_texto]
            else:
                color_foco = "black"

            if estado_texto.startswith("Intermitente"):
                if self.fase % 2 == 1:
                    color_foco = "black"

            elif estado_texto == "Patron RGB":
                indice_color = (self.fase + i) % len(self.secuencia_rgb)
                color_foco = self.secuencia_rgb[indice_color]

            colores_para_pintar.append(color_foco)

        estado_brillo = self.control_brillo.obtener_salida()
        self.vista.pintar_focos(colores_para_pintar, estado_brillo)
