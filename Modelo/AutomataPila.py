from Modelo.MaquinaDeMoore import MaquinaDeMoore

class AutomataDePila(MaquinaDeMoore):
    def __init__(self, automataFinitoDeterministico, salidas_automata, verbose=True):
        super().__init__(automataFinitoDeterministico, salidas_automata, verbose=verbose)
        self.pila = []

    def procesar_entrada(self, simbolo, verbose=None):
        if verbose is None:
            verbose = self.verbose
        transiciones_disponibles = self.AFD.transitions.get(self.estado_actual, {})

        if simbolo in transiciones_disponibles:
            if verbose:
                print(f"Agregando tu posicion actual a la pila {self.obtener_estado_actual()}")
            self.pila.append(self.estado_actual)
        return super().procesar_entrada(simbolo, verbose=verbose)

    def retroceder(self, verbose=None):
        if verbose is None:
            verbose = self.verbose
        if len(self.pila) > 0:
            self.estado_actual = self.pila.pop()
            if verbose:
                print(f"Deshacer: Volviste al estado {self.obtener_estado_actual()}")
            return self.salidas[self.estado_actual]
        else:
            if verbose:
                print("No hay historial")
            return None
