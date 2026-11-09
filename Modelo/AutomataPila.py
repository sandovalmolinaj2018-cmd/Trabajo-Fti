from Modelo.MaquinaDeMoore import MaquinaDeMoore

class AutomataDePila(MaquinaDeMoore):
    def __init__(self, automataFinitoDeterministico, salidas_automata):
        super().__init__(automataFinitoDeterministico, salidas_automata)
        self.pila = []

    def procesar_entrada(self, simbolo):
        transiciones_disponibles = self.AFD.transitions.get(self.estado_actual, {})

        if simbolo in transiciones_disponibles:
            print(f"Agregando tu posicion actual a la pila {self.obtener_estado_actual()}")
            self.pila.append(self.estado_actual)
        return super().procesar_entrada(simbolo)

    def retroceder(self):
        if len(self.pila) > 0:
            self.estado_actual = self.pila.pop()
            print(f"Deshacer: Volviste al estado {self.obtener_estado_actual()}")
            return self.salidas[self.estado_actual]
        else:
            print("No hay historial")
            return None