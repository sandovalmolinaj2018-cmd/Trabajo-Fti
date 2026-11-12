import json
import os
from typing import Optional, Dict, Tuple, Any
from Modelo.foco import Foco
from Modelo.brillo import Brillo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PRESETS_FILE = os.path.join(BASE_DIR, "presets.json")

class ControladorTiraLed:
    def __init__(self, vista: Any, archivo_presets: Optional[str] = DEFAULT_PRESETS_FILE):
        self.vista = vista
        self.vista.set_controlador(self)

        # Creacion tira led
        self.cantidad_focos = 5
        self.tira_focos = []
        for i in range(self.cantidad_focos):
            self.tira_focos.append(Foco(verbose=(i == 0)))

        self.control_brillo = Brillo()

        # Almacenamiento de presets de iluminación
        self.archivo_presets: Optional[str] = archivo_presets
        self.presets: Dict[int, Optional[Tuple[str, str, str, str]]] = {1: None, 2: None, 3: None}
        self.cargar_presets_desde_disco()

        # Animación (intermitente y RGB)
        self.fase = 0
        self.intervalo_ms = 500
        self.secuencia_rgb = ["red", "green", "blue"]

        # Traduccion entre el modelo y la vista
        # (los intermitentes guardan su color "base", el parpadeo se resuelve al pintar)
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

    def iniciar(self):
        self.vista.dibujar_tira(self.cantidad_focos)
        # Sincronizar etiquetas de presets guardados previamente
        for slot, val in self.presets.items():
            if val is not None and self.vista and hasattr(self.vista, 'actualizar_texto_preset'):
                self.vista.actualizar_texto_preset(slot, f"⚡ P{slot}: {val[2]} ({val[3]})")
        self.actualizar_pantalla()
        self.vista.programar(self.intervalo_ms, self.animar)

    def animar(self):
        # Se llama sola cada intervalo_ms
        self.fase += 1
        self.actualizar_pantalla()
        self.vista.programar(self.intervalo_ms, self.animar)

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
                self.fase = 0  # RGB arranca siempre desde el principio
            if comando == 'a':
                self.control_brillo.fijar_estado(self.control_brillo.AFD.initial_state)

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

        estado_brillo = self.control_brillo.obtener_estado_actual()
        self.vista.actualizar_luces(colores_para_pintar, estado_brillo)

    def refrescar(self):
        self.actualizar_pantalla()

    def guardar_preset(self, slot: Any):
        if isinstance(slot, str) and slot.isdigit():
            slot = int(slot)

        if not isinstance(slot, int) or slot not in self.presets:
            print(f"Error: Slot {slot} inválido. Debe ser 1, 2 o 3.")
            return False

        if self.tira_focos[0].estado_actual == 'q0':
            print("Advertencia: No se puede guardar un preset con la tira apagada. Por favor, primero enciende los focos antes de utilizar esa función.")
            if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
                self.vista.mostrar_mensaje_preset("⚠️ Tira apagada: Enciende los focos primero.", es_error=True)
            return False

        estado_foco = str(self.tira_focos[0].estado_actual)
        estado_brillo = str(self.control_brillo.estado_actual)
        nombre_color = str(self.tira_focos[0].obtener_estado_actual())
        nombre_brillo = str(self.control_brillo.obtener_estado_actual())

        self.presets[slot] = (estado_foco, estado_brillo, nombre_color, nombre_brillo)
        print(f"Preset {slot} guardado: {nombre_color} ({nombre_brillo})")

        self.guardar_presets_en_disco()

        texto_preset = f"⚡ P{slot}: {nombre_color} ({nombre_brillo})"
        if self.vista and hasattr(self.vista, 'actualizar_texto_preset'):
            self.vista.actualizar_texto_preset(slot, texto_preset)

        if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
            self.vista.mostrar_mensaje_preset(f"✅ Preset {slot} guardado: {nombre_color} ({nombre_brillo})", es_error=False)

        return True

    def cargar_preset(self, slot: Any):
        if isinstance(slot, str) and slot.isdigit():
            slot = int(slot)

        if not isinstance(slot, int) or slot not in self.presets:
            print(f"Advertencia: El slot {slot} no contiene un preset guardado.")
            if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
                self.vista.mostrar_mensaje_preset(f"⚠️ Slot {slot} vacío: Guarda un preset primero.", es_error=True)
            return False

        preset_data = self.presets[slot]
        if preset_data is None:
            print(f"Advertencia: El slot {slot} no contiene un preset guardado.")
            if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
                self.vista.mostrar_mensaje_preset(f"⚠️ Slot {slot} vacío: Guarda un preset primero.", es_error=True)
            return False

        if self.tira_focos[0].estado_actual == 'q0':
            print("Advertencia: La tira está apagada. Por favor, primero enciende los focos antes de utilizar esa función.")
            if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
                self.vista.mostrar_mensaje_preset("⚠️ Tira apagada: Enciende los focos primero.", es_error=True)
            return False

        estado_foco, estado_brillo, nombre_color, nombre_brillo = preset_data

        for i, foco in enumerate(self.tira_focos):
            foco.restaurar_estado(estado_foco, apilar_previo=True, verbose=(i == 0))

        self.control_brillo.fijar_estado(estado_brillo)
        self.fase = 0
        self.refrescar()

        if self.vista and hasattr(self.vista, 'mostrar_mensaje_preset'):
            self.vista.mostrar_mensaje_preset(f"⚡ Preset {slot} cargado: {nombre_color} ({nombre_brillo})", es_error=False)

        return True

    def guardar_presets_en_disco(self):
        """Serializa los presets a un vector de hashmaps en presets.json."""
        if not self.archivo_presets:
            return
        datos = []
        for slot in (1, 2, 3):
            val = self.presets.get(slot)
            if val is not None:
                datos.append({
                    "slot": slot,
                    "estado_foco": val[0],
                    "estado_brillo": val[1],
                    "nombre_color": val[2],
                    "nombre_brillo": val[3]
                })
            else:
                datos.append({
                    "slot": slot,
                    "estado_foco": None,
                    "estado_brillo": None,
                    "nombre_color": None,
                    "nombre_brillo": None
                })
        try:
            with open(self.archivo_presets, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar presets en disco: {e}")

    def cargar_presets_desde_disco(self):
        """Recupera los presets desde presets.json al arrancar el programa."""
        if not self.archivo_presets or not os.path.exists(self.archivo_presets) or os.path.getsize(self.archivo_presets) == 0:
            return
        try:
            with open(self.archivo_presets, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    for item in datos:
                        if not isinstance(item, dict):
                            continue
                        slot = item.get("slot")
                        if isinstance(slot, str) and slot.isdigit():
                            slot = int(slot)
                        if isinstance(slot, int) and slot in self.presets and item.get("estado_foco") is not None:
                            self.presets[slot] = (
                                str(item["estado_foco"]),
                                str(item["estado_brillo"]),
                                str(item["nombre_color"]),
                                str(item["nombre_brillo"])
                            )
        except Exception as e:
            print(f"No se pudieron cargar presets desde disco: {e}")