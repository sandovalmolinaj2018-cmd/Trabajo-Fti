class MaquinaDeMoore:
    def __init__(self, automataFinitoDeterministico, salidas_automata, verbose=True): ##Constructor
        self.AFD = automataFinitoDeterministico
        self.salidas = salidas_automata
        self.estado_actual = self.AFD.initial_state
        self.verbose = verbose

    def procesar_entrada(self, simbolo, verbose=None):
        if verbose is None:
            verbose = self.verbose
        transiciones_disponibles = self.AFD.transitions.get(self.estado_actual, {})

        if simbolo in transiciones_disponibles:
            self.estado_actual = transiciones_disponibles[simbolo]
            if verbose:
                print(f"Cambios de estado a {self.obtener_estado_actual()}")
            return self.salidas[self.estado_actual]
        else:
            if verbose:
                print(f"No se puede transicionar a ese estado, seguis en el estado {self.estado_actual}")
            return None

    def obtener_estado_actual(self):
        return self.salidas[self.estado_actual]
