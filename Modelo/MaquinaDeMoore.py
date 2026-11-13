class MaquinaDeMoore:
    def __init__(self, automataFinitoDeterministico, salidas_automata, verbose=True):
        self.AFD = automataFinitoDeterministico
        self.salidas = salidas_automata
        self.estado_actual = self.AFD.initial_state
        self.verbose = verbose

    def puede_transicionar(self, simbolo):
        transiciones_disponibles = self.AFD.transitions.get(self.estado_actual, {})
        return simbolo in transiciones_disponibles

    def obtener_transiciones_posibles(self):
        return self.AFD.transitions.get(self.estado_actual, {})

    def procesar_entrada(self, simbolo, verbose=None):
        if verbose is None:
            verbose = self.verbose

        if self.puede_transicionar(simbolo):
            self.estado_actual = self.AFD.transitions[self.estado_actual][simbolo]
            if verbose:
                print(f"[Moore] Cambio de estado a {self.estado_actual} ({self.obtener_salida_actual()})")
            return self.obtener_salida_actual()
        else:
            if verbose:
                print(
                    f"[Moore] Transición no definida para '{simbolo}' "
                    f"desde {self.estado_actual} ({self.obtener_salida_actual()})"
                )
            return None

    def obtener_estado_actual(self):
        return self.estado_actual

    def obtener_salida_actual(self):
        return self.salidas[self.estado_actual]