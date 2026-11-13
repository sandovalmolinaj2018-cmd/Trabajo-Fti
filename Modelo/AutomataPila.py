from automata.pda.dpda import DPDA


class AutomataDePila:
    """
    Autómata de Pila Determinista (DPDA) formal para el control de iluminación.
    - Criterio de Aceptación: Pila Vacía (empty_stack).
    - Memoria de encendido: Al apagar ('a'), el autómata guarda el estado activo
      en la pila. Al reencender ('e'), recupera el estado previo y desapila (pop),
      vaciando la pila al completar el ciclo.
    """
    SIMBOLO_INICIAL_PILA = 'Z'

    # Mapeo biyectivo de estados operativos a símbolos de pila de un carácter (compatibilidad JFLAP)
    MAP_ESTADO_PILA = {
        'q1': '1',
        'q2': '2',
        'q3': '3',
        'q4': '4',
        'q5': '5',
        'q6': '6',
        'q7': '7',
        'q8': '8',
        'q9': '9',
        'q10': 'A',
    }
    MAP_PILA_ESTADO = {v: k for k, v in MAP_ESTADO_PILA.items()}

    def __init__(self, dpda: DPDA, salidas_automata: dict, verbose=True):
        self.DPDA = dpda
        self.salidas = salidas_automata
        self.estado_actual = self.DPDA.initial_state
        self.verbose = verbose
        self.pila = [self.SIMBOLO_INICIAL_PILA]
        self.historial_entrada = []

    def puede_transicionar(self, simbolo):
        """Verifica si existe una transición definida para el estado actual y el tope de pila."""
        tope_pila = self.pila[-1] if self.pila else self.SIMBOLO_INICIAL_PILA
        trans_estado = self.DPDA.transitions.get(self.estado_actual, {})
        return tope_pila in trans_estado.get(simbolo, {})

    def obtener_transiciones_posibles(self):
        """Devuelve un diccionario {simbolo: estado_destino} válidas con el tope actual."""
        tope_pila = self.pila[-1] if self.pila else self.SIMBOLO_INICIAL_PILA
        trans_estado = self.DPDA.transitions.get(self.estado_actual, {})
        posibles = {}
        for simbolo, trans_simbolo in trans_estado.items():
            if tope_pila in trans_simbolo:
                estado_destino, _ = trans_simbolo[tope_pila]
                posibles[simbolo] = estado_destino
        return posibles

    def procesar_entrada(self, simbolo, verbose=None):
        """
        Ejecuta un paso de transición en el DPDA:
        Lee símbolo -> hace POP del tope -> hace PUSH de la cadena resultante -> actualiza estado.
        En modo interactivo, si la pila queda vacía tras un reencendido con memoria,
        se restaura el símbolo base 'Z' para permitir interacción continua.
        """
        if verbose is None:
            verbose = self.verbose

        if not self.puede_transicionar(simbolo):
            if verbose:
                tope = self.pila[-1] if self.pila else None
                print(
                    f"[DPDA] Transición no definida para '{simbolo}' desde {self.estado_actual} "
                    f"con tope '{tope}' | Configuración: {self.formatear_configuracion()}"
                )
            return None

        tope_pila = self.pila[-1]
        nuevo_estado, apilar = self.DPDA.transitions[self.estado_actual][simbolo][tope_pila]

        # Operación formal de Pila: POP del tope actual
        self.pila.pop()
        # PUSH de los nuevos símbolos (en orden inverso para preservar la cima)
        for simb_pila in reversed(apilar):
            self.pila.append(simb_pila)

        self.estado_actual = nuevo_estado
        self.historial_entrada.append(simbolo)

        # En modo interactivo continuo: si la pila quedó vacía tras completar un ciclo de vaciado,
        # restablecemos el símbolo base para que la GUI y el usuario sigan operando sin interrupción.
        pila_vaciada = len(self.pila) == 0

        if verbose:
            print(
                f"[DPDA] Entrada '{simbolo}' -> {self.estado_actual} ({self.obtener_salida_actual()}) | "
                f"Configuración: {self.formatear_configuracion()}"
            )

        if pila_vaciada:
            self.pila.append(self.SIMBOLO_INICIAL_PILA)
            if verbose:
                print(
                    f"[DPDA] Pila vacía (secuencia aceptada) -> "
                    f"Restaurando base '{self.SIMBOLO_INICIAL_PILA}' para modo continuo: "
                    f"{self.formatear_configuracion()}"
                )
        return self.obtener_salida_actual()

    def obtener_estado_actual(self):
        """Devuelve el identificador del estado actual (ej. 'q0', 'q1')."""
        return self.estado_actual

    def obtener_salida_actual(self):
        """Devuelve la salida de la máquina de Moore asociada al estado actual (ej. 'Blanco')."""
        return self.salidas[self.estado_actual]

    def obtener_configuracion(self):
        """Devuelve la descripción instantánea (estado_actual, copia_pila)."""
        return (self.estado_actual, list(self.pila))

    def formatear_configuracion(self):
        """Representa la configuración (q, [tope ... base])."""
        pila_str = " ".join(reversed(self.pila)) if self.pila else "λ"
        return f"({self.estado_actual}, [{pila_str}])"

    def aceptar_cadena(self, cadena):
        """
        Evalúa formalmente si una palabra w ∈ ΣE* es aceptada por Pila Vacía.
        Delega directamente en el DPDA formal de automata-lib.
        """
        return self.DPDA.accepts_input(cadena)

    def simular_cadena(self, cadena):
        """Devuelve la traza paso a paso de configuraciones del DPDA para una cadena w."""
        pasos = []
        for config in self.DPDA.read_input_stepwise(cadena):
            pasos.append((config.state, config.remaining_input, list(config.stack.stack)))
        return pasos
