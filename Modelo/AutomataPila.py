from automata.pda.dpda import DPDA  # Libreria del automata de pila


class AutomataDePila():
    Inicial_Pila = 'Z'

    def __init__(self, automata, diccionario_salida, diccionario_pila, mostrar_mensaje_terminals=True):
        self.automata_pila = automata
        self.salidas = diccionario_salida
        self.diccionario_pila = diccionario_pila
        self.estado_actual = self.automata_pila.initial_state
        self.mostrar_terminal = mostrar_mensaje_terminals
        self.pila = [self.Inicial_Pila]
        self.historial_entrada = []

    def obtener_tope(self):
        if len(self.pila) > 0:
            tope_pila = len(self.pila) - 1
            if self.mostrar_terminal == True:
                print("El tope de la pila es: " + str(self.pila[tope_pila]))
            return self.pila[tope_pila]
        else:
            if self.mostrar_terminal == True:
                print("El tope es el estado inicial")
            return self.Inicial_Pila

    def autorizacion_transicionar(self, entrada):
        tope_pila = self.obtener_tope()
        if self.estado_actual in self.automata_pila.transitions:
            transiciones = self.automata_pila.transitions[self.estado_actual]
        else:
            transiciones = {}

        if entrada in transiciones:
            transiciones_simbolo = transiciones[entrada]
        else:
            transiciones_simbolo = {}

        if tope_pila in transiciones_simbolo:
            return True
        else:
            return False

    def obtener_transiciones_posibles(self):
        tope_pila = self.obtener_tope()
        if self.estado_actual in self.automata_pila.transitions:
            transiciones = self.automata_pila.transitions[self.estado_actual]
        else:
            transiciones = {}

        posibles = {}

        for simbolo in transiciones:
            transicion_simbolo = transiciones[simbolo]
            if tope_pila in transicion_simbolo:
                tupla = transicion_simbolo[tope_pila]
                destino = tupla[0]
                posibles[simbolo] = destino

        return posibles

    def procesar_entrada(self, entrada, mostrar_mensaje_terminal=None):
        if mostrar_mensaje_terminal is None:
            mostrar_mensaje_terminal = self.mostrar_terminal

        valido = self.autorizacion_transicionar(entrada)
        tope_pila = self.obtener_tope()
        if valido == False:
            if mostrar_mensaje_terminal == True:
                print("No hay transiciones para la entrada: " + str(entrada) + " En el estado: " + str(self.estado_actual) + " con tope de la pila: " + str(tope_pila))
            return None


        reaccion = self.automata_pila.transitions[self.estado_actual][entrada][tope_pila]
        nuevo_estado = reaccion[0]
        simbolo_apilar = reaccion[1]

        self.pila.pop()
        lista_invertida = list(simbolo_apilar)
        lista_invertida.reverse()
        for simbolo_pila in lista_invertida:
            self.pila.append(simbolo_pila)


        self.estado_actual = nuevo_estado
        self.historial_entrada.append(entrada)

        if len(self.pila) == 0:
            pila_vacia = True
        else:
            pila_vacia = False


        if mostrar_mensaje_terminal == True:
            print("Entrada: " + str(entrada) + " Estado: " + str(self.estado_actual) + " Salida: " + str(self.obtener_salida_actual()))

        if pila_vacia == True:
            self.pila.append(self.Inicial_Pila)

        return self.obtener_salida_actual()

    def retroceder(self, mostrar_mensajes=None):
        return self.procesar_entrada('d', mostrar_mensajes)

    def reiniciar_pila(self):
        self.estado_actual = self.automata_pila.initial_state
        self.pila = [self.Inicial_Pila]

    def obtener_estado_actual(self):
        return self.estado_actual

    def obtener_salida_actual(self):
        return self.salidas[self.estado_actual]

    def obtener_configuracion(self):
        copia_pila = list(self.pila)
        return (self.estado_actual, copia_pila)

    def ver_pila(self):
        if len(self.pila) > 0:
            copia_invertida_pila = list(self.pila)
            copia_invertida_pila.reverse()
            for i in range(len(copia_invertida_pila)):
                if self.mostrar_terminal == True:
                    print(copia_invertida_pila[i])
        else:
            if self.mostrar_terminal == True:
                print("Pila vacia")
        return None

    def aceptar_cadena(self, cadena):
        return self.automata_pila.accepts_input(cadena)