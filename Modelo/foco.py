from automata.pda.dpda import DPDA
from Modelo.AutomataPila import AutomataDePila


class Foco(AutomataDePila):
    """
    Representa el canal de iluminación gobernado por un Autómata de Pila Determinista (DPDA)
    con salidas de Máquina de Moore y aceptación por Pila Vacía.
    """

    def __init__(self, verbose=True):
        estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
        alfabeto_entrada = {'e', 'a', 'b', 'r', 'v', 'z', 'p', 'i', 'g'}
        alfabeto_pila = {'Z'} | set(self.MAP_ESTADO_PILA.values())

        # Grafo de transiciones cromáticas y de modos cuando la tira está encendida
        grafo_iluminacion = {
            'q1': {'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5', 'g': 'q9'},
            'q2': {'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'},
            'q3': {'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'},
            'q4': {'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'},
            'q5': {'b': 'q1'},
            'q6': {'r': 'q2'},
            'q7': {'v': 'q3'},
            'q8': {'z': 'q4'},
            'q9': {'p': 'q10'},
            'q10': {'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'g': 'q9'},
        }

        transiciones = {s: {} for s in estados}

        # Transiciones desde q0 (Apagado):
        # 1. Arranque en frío: 'e' con pila 'Z' enciende al estado base Blanco (q1)
        transiciones['q0']['e'] = {'Z': ('q1', ('Z',))}
        # 2. Apagado en frío: 'a' con pila 'Z' desapila 'Z' y vacía la pila
        transiciones['q0']['a'] = {'Z': ('q0', ())}

        # 3. Reencendido con memoria y apagado definitivo desde q0:
        for estado_previo, simb_pila in self.MAP_ESTADO_PILA.items():
            # 'e' recupera el estado previo y hace POP, vaciando la pila (aceptación por pila vacía)
            transiciones['q0']['e'][simb_pila] = (estado_previo, ())
            # 'a' apaga definitivamente desapilando la memoria
            transiciones['q0']['a'][simb_pila] = ('q0', ())

        # Transiciones desde estados encendidos (q1 a q10):
        for q in estados - {'q0'}:
            simb_memoria = self.MAP_ESTADO_PILA[q]
            # 'a' apaga hacia q0 y guarda en la cima de la pila el estado actual
            transiciones[q]['a'] = {'Z': ('q0', (simb_memoria,))}

            # Transiciones de cambio de color / patrón: conservan la base 'Z'
            for simbolo_in, estado_dest in grafo_iluminacion.get(q, {}).items():
                transiciones[q][simbolo_in] = {'Z': (estado_dest, ('Z',))}

        dpda_foco = DPDA(
            states=estados,
            input_symbols=alfabeto_entrada,
            stack_symbols=alfabeto_pila,
            transitions=transiciones,
            initial_state='q0',
            initial_stack_symbol=self.SIMBOLO_INICIAL_PILA,
            final_states=set(),
            acceptance_mode='empty_stack',
        )

        salidas_moore = {
            'q0': "Apagado",
            'q1': "Blanco",
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

        super().__init__(dpda_foco, salidas_moore, verbose=verbose)

    def posibles_caminos(self):
        """Devuelve las salidas descriptivas de las transiciones alcanzables desde el estado y tope actual."""
        return [
            self.salidas[destino]
            for destino in self.obtener_transiciones_posibles().values()
        ]
