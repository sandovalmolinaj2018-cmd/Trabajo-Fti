from automata.fa.dfa import DFA
from Modelo.AutomataPila import AutomataDePila

class Foco(AutomataDePila):
    def __init__(self):
        luces_nfa = DFA(
            states={'q0','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'},
            input_symbols={'e','a','b','r','v','z','p','i','g'},
            transitions={
                    'q0': {                     
                        'e': 'q1'            
                    },
                    'q1': {
                        'a': 'q0', 'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5', 'g': 'q9'
                    },
                    'q2': {
                        'a': 'q0', 'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'
                    },
                    'q3': {
                        'a': 'q0', 'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'
                    },
                    'q4': {
                        'a': 'q0', 'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'
                    },
                    'q5': {'a': 'q0', 'b': 'q1'},
                    'q6': {'a': 'q0', 'r': 'q2'},
                    'q7': {'a': 'q0', 'v': 'q3'},
                    'q8': {'a': 'q0', 'z': 'q4'},
                    'q9': {'a': 'q0', 'p': 'q10'},
                    'q10': {'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'a': 'q0', 'g': 'q9'}
                },
                initial_state='q0',
                final_states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
                allow_partial=True 
            )
        

        traducido ={ 
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

        super().__init__(luces_nfa,traducido)

    def posibles_caminos(self):
        caminos = []
        nodo_actual = self.AFD.transitions.get(self.estado_actual, {})
        for camino in nodo_actual.values():
            estado = self.salidas[camino]
            caminos.append(estado)

        return caminos