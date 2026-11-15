from automata.pda.dpda import DPDA
from automata.fa.nfa import NFA
from Modelo.AutomataPila import AutomataDePila


class Foco(AutomataDePila):

    def __init__(self, mostrar_mensajes=True):
        estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
        alfabeto_entrada = {'e', 'a', 'b', 'r', 'v', 'z', 'p', 'i', 'g', 'd'}

        mapa_pila_estados = {
            'q1': '1', 'q2': '2', 'q3': '3', 'q4': '4', 'q5': '5',
            'q6': '6', 'q7': '7', 'q8': '8', 'q9': '9', 'q10': 'A'
        }

        alfabeto_pila = {'Z'}
        for estado_clave in mapa_pila_estados:
            simbolo_valor = mapa_pila_estados[estado_clave]
            alfabeto_pila.add(simbolo_valor)

        grafo_iluminacion = {
            'q1': {'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5', 'g': 'q9'},
            'q2': {'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'},
            'q3': {'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'},
            'q4': {'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'},
            'q5': {'b': 'q1', 'p': 'q10'},
            'q6': {'r': 'q2', 'p': 'q10'},
            'q7': {'v': 'q3', 'p': 'q10'},
            'q8': {'z': 'q4', 'p': 'q10'},
            'q9': {'p': 'q10'},
            'q10': {'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'g': 'q9'}
        }

        self.afnd_selector_patrones = NFA(
            states={'q10', 'q5', 'q6', 'q7', 'q8', 'q9'},
            input_symbols={'i', 'g'},
            transitions={
                'q10': {
                    'i': {'q5', 'q6', 'q7', 'q8'},
                    'g': {'q9'}
                }
            },
            initial_state='q10',
            final_states={'q5', 'q6', 'q7', 'q8', 'q9'}
        )

        transiciones = {}
        for estado in estados:
            transiciones[estado] = {}

        transiciones['q0']['e'] = {}
        transiciones['q0']['a'] = {}
        transiciones['q0']['e']['Z'] = ('q1', ('Z',))
        transiciones['q0']['a']['Z'] = ('q0', ())

        for estado_previo in mapa_pila_estados:
            simbolo_pila = mapa_pila_estados[estado_previo]
            transiciones['q0']['e'][simbolo_pila] = (estado_previo, ())
            transiciones['q0']['a'][simbolo_pila] = ('q0', ())

        for estado_origen in estados:
            if estado_origen != 'q0':
                simbolo_memoria = mapa_pila_estados[estado_origen]

                transiciones[estado_origen]['a'] = {}
                transiciones[estado_origen]['d'] = {}

                for tope_actual in alfabeto_pila:
                    transiciones[estado_origen]['a'][tope_actual] = ('q0', (simbolo_memoria, tope_actual))

                    if estado_origen in grafo_iluminacion:
                        caminos_estado = grafo_iluminacion[estado_origen]
                        for simbolo_in in caminos_estado:
                            estado_destino = caminos_estado[simbolo_in]
                            if simbolo_in not in transiciones[estado_origen]:
                                transiciones[estado_origen][simbolo_in] = {}
                            transiciones[estado_origen][simbolo_in][tope_actual] = (estado_destino, (simbolo_memoria, tope_actual))

                for estado_previo in mapa_pila_estados:
                    simbolo_pila = mapa_pila_estados[estado_previo]
                    transiciones[estado_origen]['d'][simbolo_pila] = (estado_previo, ())

        dpda_foco = DPDA(
            states=estados,
            input_symbols=alfabeto_entrada,
            stack_symbols=alfabeto_pila,
            transitions=transiciones,
            initial_state='q0',
            initial_stack_symbol='Z',
            final_states=set(),
            acceptance_mode='empty_stack'
        )

        salidas_moore = {
            'q0': "Apagado", 'q1': "Blanco", 'q2': "Rojo", 'q3': "Verde", 'q4': "Azul",
            'q5': "Intermitente blanco", 'q6': "Intermitente rojo", 'q7': "Intermitente verde",
            'q8': "Intermitente azul", 'q9': "Patron RGB", 'q10': "Menu Patrones"
        }

        super().__init__(
            automata=dpda_foco,
            diccionario_salida=salidas_moore,
            diccionario_pila=mapa_pila_estados,
            mostrar_mensaje_terminals=mostrar_mensajes
        )

    def posibles_caminos(self):
        caminos = []
        transiciones_validas = self.obtener_transiciones_posibles()
        for simbolo in transiciones_validas:
            estado_destino = transiciones_validas[simbolo]
            nombre_salida = self.salidas[estado_destino]
            caminos.append(nombre_salida)
        return caminos
