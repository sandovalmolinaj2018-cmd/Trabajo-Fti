##Codigo del AFND usando la libreria automata-lib
from automata.fa.dfa import DFA

# DFA que acepta strings binarios que terminan en '1'
my_dfa = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)
# Probar entradas
print(my_dfa.accepts_input('01'))      # True (termina en 1)
print(my_dfa.accepts_input('010'))     # False (termina en 0)
print(my_dfa.accepts_input('111'))     # True (termina en 1)

my_dfa.show_diagram(path="diagrama.png")

diagrama = DFA(
    states= {'q0', 'q1', 'q2'},
    input_symbols= {'0', '1'},
    transitions= {
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q2', '1': 'q1'},
        'q2': {'0': 'q2', '1': 'q2'}
    },
    initial_state= 'q0',
    final_states= {'q1'}
)