from Modelo.AutomataLinealmenteLimitado import AutomataLinealmenteLimitado


class MemoriaPresets(AutomataLinealmenteLimitado):

    def __init__(self, mostrar_mensajes=True):
        diccionario_slots = {
            'DEF': 1,
            0: 1,
            'P1': 2,
            1: 2,
            'P2': 3,
            2: 3,
            'P3': 4,
            3: 4
        }

        celda_defecto = {
            "cadena_w": "e",
            "comando_brillo": "5",
            "estado_foco": "q1",
            "estado_brillo": "q4",
            "nombre_color": "Blanco",
            "nombre_brillo": "Maximo"
        }

        valores_iniciales = {
            1: celda_defecto
        }

        super().__init__(
            cantidad=4,
            diccionario=diccionario_slots,
            valores_iniciales=valores_iniciales,
            mostrar_mensajes=mostrar_mensajes
        )
