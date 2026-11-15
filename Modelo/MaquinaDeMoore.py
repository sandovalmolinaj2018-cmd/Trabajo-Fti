class MaquinaDeMoore:
    def __init__(self, automataFinitoDeterministico, salidas_automata, mostrar_mensaje_terminal=True): ##Constructor
        self.AFD = automataFinitoDeterministico
        self.salidas = salidas_automata
        self.estado_actual = self.AFD.initial_state
        self.mostrar_mensaje_terminal = mostrar_mensaje_terminal

    def autorizado_transicion(self, simbolo):
        if simbolo in self.AFD.transitions[self.estado_actual]:
            return True
        else:
            return False

    def obtener_caminos_posibles(self):
        if self.estado_actual in self.AFD.transitions:
            return self.AFD.transitions[self.estado_actual]
        else:
            return {}

    def obtener_salida(self):
        return self.salidas[self.estado_actual]

    def transicionar(self, simbolo_entrada, mostrar_mensaje_terminal=None):
        if mostrar_mensaje_terminal is None:
            mostrar_mensaje_terminal= self.mostrar_mensaje_terminal

        if self.autorizado_transicion(simbolo_entrada):
            self.estado_actual = self.AFD.transitions[self.estado_actual][simbolo_entrada]
            if mostrar_mensaje_terminal == True:
                print("Transicion: ")
                print("Entrada: " + str(simbolo_entrada))
                print("Estado Actual " + str(self.estado_actual))
                print("Salida: " + str(self.obtener_salida()))
            return self.obtener_salida
        else:
            if mostrar_mensaje_terminal == True:
                print("La transicion no existe para la entrada de: " + str(simbolo_entrada))
                print("Seguis en " + str(simbolo_entrada))
                print("Salida: " + str(self.obtener_salida))
            return None

    def obtener_estado_actual(self):
        return self.salidas[self.estado_actual]

    def fijar_estado(self, nuevo_estado):
        if nuevo_estado in self.AFD.states:
            self.estado_actual = nuevo_estado
            print("El automata ahora se encuntra en: " + str(self.estado_actual))
            print("La salida es: " + str(self.obtener_salida))
            return True
        else:
            print("Error no se puede poner el automata en ese estado")
            return False
