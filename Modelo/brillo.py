from automata.fa.dfa import DFA
from Modelo.MaquinaDeMoore import MaquinaDeMoore


class Brillo(MaquinaDeMoore):
    def __init__(self, mostrar_mensajes=True):
        automata_brillo = DFA(
            states={'q0', 'q1', 'q2', 'q3', 'q4'},
            input_symbols={'1', '2', '3', '4', '5'},
            transitions={
                'q0': {'1': 'q0', '2': 'q1', '3': 'q2', '4': 'q3', '5': 'q4'},
                'q1': {'1': 'q0', '2': 'q1', '3': 'q2', '4': 'q3', '5': 'q4'},
                'q2': {'1': 'q0', '2': 'q1', '3': 'q2', '4': 'q3', '5': 'q4'},
                'q3': {'1': 'q0', '2': 'q1', '3': 'q2', '4': 'q3', '5': 'q4'},
                'q4': {'1': 'q0', '2': 'q1', '3': 'q2', '4': 'q3', '5': 'q4'}
            },
            initial_state='q4',
            final_states={'q0', 'q1', 'q2', 'q3', 'q4'}
        )

        salidas_brillo = {
            'q0': "Bajo",
            'q1': "Tenue",
            'q2': "Medio",
            'q3': "Alto",
            'q4': "Maximo"
        }

        super().__init__(
            automataFinitoDeterministico=automata_brillo,
            salidas_automata=salidas_brillo,
            mostrar_mensaje_terminal=mostrar_mensajes
        )
