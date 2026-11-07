class MaquinaDeMoore:
    def __init__(self, automata_dfa, diccionario_salidas):
        """
        Inicializa la Máquina de Moore con la teoría matemática y las salidas físicas.
        """
        self.motor_dfa = automata_dfa
        self.salidas = diccionario_salidas
        
        # El estado físico inicial coincide con el estado inicial del DFA matemático
        self.estado_actual = self.motor_dfa.initial_state

    def procesar_comando(self, simbolo):
        """
        Lee un comando, valida si existe una transición matemática y devuelve la salida.
        Retorna una tupla: (fue_exitoso (bool), salida_fisica_actual (str))
        """
        # 1. Buscamos qué flechas salen del estado en el que estamos parados
        transiciones_disponibles = self.motor_dfa.transitions.get(self.estado_actual, {})
        
        # 2. Si el símbolo ingresado existe en esas flechas, avanzamos
        if simbolo in transiciones_disponibles:
            self.estado_actual = transiciones_disponibles[simbolo]
            return True, self.salidas[self.estado_actual]
            
        # 3. Si el símbolo no existe o es inválido para este estado, lo rechazamos y no nos movemos
        else:
            return False, self.salidas[self.estado_actual]

    def obtener_estado_fisico(self):
        """
        Devuelve la descripción física actual sin modificar nada.
        """
        return self.salidas[self.estado_actual]