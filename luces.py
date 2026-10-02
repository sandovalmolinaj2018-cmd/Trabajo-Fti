from automata.fa.nfa import NFA

# Definición del AFND para el control de luces led del hogar
luces_nfa = NFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    input_symbols={'e', 'a', 'b', 'r', 'v', 'z', 'p', 'i', 'g'},
    transitions={
        'q0': {
            'e': {'q1', 'q2', 'q3', 'q4', 'q10'} # Al encender puede ir de forma no determinística a varios colores o patrones
        },
        'q1': {
            'a': {'q0'}, 'r': {'q2'}, 'v': {'q3'}, 'z': {'q4'}, 'p': {'q10'}, 'i': {'q5'}
        },
        'q2': {
            'a': {'q0'}, 'b': {'q1'}, 'v': {'q3'}, 'z': {'q4'}, 'p': {'q10'}, 'i': {'q6'}
        },
        'q3': {
            'a': {'q0'}, 'b': {'q1'}, 'r': {'q2'}, 'z': {'q4'}, 'p': {'q10'}, 'i': {'q7'}
        },
        'q4': {
            'a': {'q0'}, 'b': {'q1'}, 'r': {'q2'}, 'v': {'q3'}, 'p': {'q10'}, 'i': {'q8'}
        },
        'q5': {'a': {'q0'}, 'b': {'q1'}},
        'q6': {'a': {'q0'}, 'r': {'q2'}},
        'q7': {'a': {'q0'}, 'v': {'q3'}},
        'q8': {'a': {'q0'}, 'z': {'q4'}},
        'q9': {'a': {'q0'}, 'p': {'q10'}},
        'q10': {'b': {'q5'}, 'r': {'q6'}, 'v': {'q7'}, 'z': {'q8'}, 'a': {'q0'}, 'g': {'q9'}}
    },
    initial_state='q0',
    final_states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'}
)


#revisa si la cadena es valida
if luces_nfa.accepts_input('ebzpb'):
    print("La cadena es aceptada")
else:
    print("Cadena no aceptada")

#dice el estado final
estados_finales = luces_nfa.read_input('ebzpb')
print(estados_finales)

#permite ver todos los caminos cuando estamos en alguna estado
transiciones_q0 = luces_nfa.transitions.get('q5', {})

for simbolo, destinos in transiciones_q0.items():
    print(f"Símbolo '{simbolo}' te lleva a -> {destinos}")

#Revisa todas las posibilidades a medida que se avanza con la cadena
for paso, estados in enumerate(luces_nfa.read_input_stepwise('ebzpb')):
    print(f"Paso {paso}: {estados}")


