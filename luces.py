from automata.fa.nfa import NFA

luces_nfa = NFA(
    states={'q0','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'},
    input_symbols={'e','a','b','r','v','z','p','i','g'},
    transitions={
        'q0': {                     
            'e': {'q1'}            
        },
        'q1': {
            'a': {'q0'}, 'r': {'q2'}, 'v': {'q3'}, 'z': {'q4'}, 'p': {'q10'},'i': {'q5'},'g': {'q9'}
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

luces_nfa.show_diagram(path="diagrama.png")

def traduccionEstado(cadenaPalabra: str): 
   estadoActual = luces_nfa.read_input(cadenaPalabra)

   traducido ={ 
        frozenset({'q1'}): "Blanco",
        frozenset({'q0'}): "Apagado",
        frozenset({'q2'}): "Rojo",
        frozenset({'q3'}): "Verde",
        frozenset({'q4'}): "Azul",
        frozenset({'q5'}): "Intermitente blanco",
        frozenset({'q6'}): "Intermitente rojo",
        frozenset({'q7'}): "Intermitente verde",
        frozenset({'q8'}): "Intermitente azul",
        frozenset({'q9'}): "Patron RGB",
        frozenset({'q10'}): "Menu Patrones",
    }
   print(estadoActual)
   return traducido.get(estadoActual, "Error")


comandos= """ 
e = Encender  
a = Apagar  
b = Blanco  
r = Rojo  
v = Verde  
z = Azul  
p = Menu de Patrones  
i = Intermitente  
g = RGB  
salir = salir """


cadenaPalabra = ""
ejecucion = True
print("Bienvenido, te presentamos que significa cada abreviatura: ")
print(comandos)
while ejecucion:

    letraActual = input("Ingrese la letra o comando: ").strip()
    if letraActual != "salir":
        cadenaPalabra = cadenaPalabra + letraActual   
        print(f"Tu palabra formada por ahora es: {cadenaPalabra}")
        if luces_nfa.accepts_input(cadenaPalabra):
            print(f"La palabra es aceptada, actualmente te encuntras en el estado de: {traduccionEstado(cadenaPalabra)}")
        else:
            print(f"La palabra fue rechazada")   
    else:
        ejecucion = False

print(f"Hasta luego!!!")     

