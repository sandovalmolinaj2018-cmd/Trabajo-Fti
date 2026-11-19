from automata.fa.dfa import DFA
from automata.pda.dpda import DPDA
from Modelo.AutomataPila import AutomataDePila


class Foco(AutomataDePila):
    def __init__(self, mostrar_mensajes=True):
        luces_dfa = DFA(
            states={'q0','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'},
            input_symbols={'e','a','b','r','v','z','p','i','g'},
            transitions={
                'q0': {'e': 'q1'},
                'q1': {'a': 'q0', 'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5'},
                'q2': {'a': 'q0', 'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'},
                'q3': {'a': 'q0', 'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'},
                'q4': {'a': 'q0', 'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'},
                'q5': {'a': 'q0', 'b': 'q1', 'p': 'q10'},
                'q6': {'a': 'q0', 'r': 'q2','p': 'q10'},
                'q7': {'a': 'q0', 'v': 'q3', 'p': 'q10'},
                'q8': {'a': 'q0', 'z': 'q4', 'p': 'q10'},
                'q9': {'a': 'q0', 'p': 'q10', 'p': 'q10'},
                'q10': {'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'a': 'q0', 'g': 'q9'}
            },
            initial_state='q0',
            final_states={'q0','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'},
            allow_partial=True
        )
        self.AFD = luces_dfa
        
        self.diccionario_pila = {'q1': '1', 'q2': '2', 'q3': '3', 'q4': '4', 'q5': '5','q6': '6', 'q7': '7', 'q8': '8', 'q9': '9', 'q10': 'A'}
        alfabeto_pila = set(self.diccionario_pila.values())
        alfabeto_pila.add('Z')
        alfabeto_entrada = set(luces_dfa.input_symbols)
        alfabeto_entrada.add('d')

        transiciones = {}
        for estado in luces_dfa.states:
            transiciones[estado] = {}

        transiciones['q0']['e'] = {'Z': ('q1', ('Z',))}
        for estado_previo in self.diccionario_pila:
            simbolo = self.diccionario_pila[estado_previo]
            transiciones['q0']['e'][simbolo] = (estado_previo, ())

        for estado in self.diccionario_pila:
            simbolo_memoria = self.diccionario_pila[estado]
            caminos = luces_dfa.transitions[estado]

            for letra in caminos:
                destino = caminos[letra]
                transiciones[estado][letra] = {}
                for tope in alfabeto_pila:
                    transiciones[estado][letra][tope] = (destino, (simbolo_memoria, tope))
                    
            transiciones[estado]['d'] = {}
            for estado_previo in self.diccionario_pila:
                simbolo = self.diccionario_pila[estado_previo]
                transiciones[estado]['d'][simbolo] = (estado_previo, ())

        dpda_foco = DPDA(
            states=set(luces_dfa.states),
            input_symbols=alfabeto_entrada,
            stack_symbols=alfabeto_pila,
            transitions=transiciones,
            initial_state='q0',
            initial_stack_symbol='Z',
            final_states=set(),
            acceptance_mode='empty_stack'
        )

        traducido = {
            'q1': "Blanco",
            'q0': "Apagado",
            'q2': "Rojo",
            'q3': "Verde",
            'q4': "Azul",
            'q5': "Intermitente blanco",
            'q6': "Intermitente rojo",
            'q7': "Intermitente verde",
            'q8': "Intermitente azul",
            'q9': "Patron RGB",
            'q10': "Menu Patrones",
        }

        super().__init__(
            automata=dpda_foco,
            diccionario_salida=traducido, #Maquina de moore
            diccionario_pila=self.diccionario_pila,
            mostrar_mensaje_terminals=mostrar_mensajes
        )

    def posibles_caminos(self):
        caminos = []
        nodo_actual = self.AFD.transitions.get(self.estado_actual, {})
        for camino in nodo_actual.values():
            estado = self.salidas[camino]
            caminos.append(estado)

        return caminos

    def aceptar_pila_vacia(self,cadena):
        if not cadena or not isinstance(cadena, str):
            return False
        pila_auxiliar = [self.Inicial_Pila]
        for simbolo in reversed(cadena):
            pila_auxiliar.append(simbolo)

        estado_actual = self.AFD.initial_state

        while pila_auxiliar[-1] != self.Inicial_Pila:
            tope_pila = pila_auxiliar[-1]
            caminos_posibles = self.AFD.transitions.get(estado_actual, {})
            if tope_pila in caminos_posibles:
                estado_actual = caminos_posibles[tope_pila]
                pila_auxiliar.pop()
            else:
                return False

        if pila_auxiliar[-1] == self.Inicial_Pila and estado_actual in self.AFD.final_states:
            return True
        else:
            return False