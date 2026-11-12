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

    def restaurar_estado(self, nuevo_estado, apilar_previo=True, verbose=None):
        if verbose is None:
            verbose = self.verbose

        if nuevo_estado not in self.AFD.states:
            if verbose:
             print(f"No se puede transicionar a ese estado, seguis en el estado {self.estado_actual}")
            return False

        if apilar_previo:
            if verbose:
             print(f"Agregando tu posicion actual a la pila {self.obtener_estado_actual()}")
            self.pila.append(self.estado_actual)

        self.estado_actual = nuevo_estado
        if verbose:
            print(f"Cambios de estado a {self.obtener_estado_actual()}")
        return True