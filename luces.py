from automata.fa.nfa import NFA

# Definición del AFND para el control de luces led del hogar
luces_nfa = NFA(
    states={'q0','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'},
    input_symbols={'e','a','b','r','v','z','p','i','g'},
    transitions={
        'q0': {                     
            'e': {'q1'}            
        },
        'q1': {
            'a': {'q0'}, 'b': {'q1'}, 'r': {'q2'}, 'v': {'q3'}, 'z': {'q4'}, 'p': {'q10'},'i': {'q5'},'g': {'q9'}
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


# traducido = {
#     "q0": "Apagado",
#     "q1": "Blanco",
#     "q2": "Rojo",
#     "q3": "Verde",
#     "q4": "Azul",
#     "q5": "Intermitente blanco",
#     "q6": "Intermitente rojo",
#     "q7": "Intermitente verde",
#     "q8": "Intermitente azul",
#     "q9": "Patron RGB",
#     "q10": "Menu Patrones",
# }

def traduccionEstado(cadenaPalabra: str): #Funcion que traduce el reado_input para poder ver a que hace referencia el estado
   estadoActual = luces_nfa.read_input(cadenaPalabra)

   traducido ={ #Diccionario en donde estan todos los posibles estados
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

    
         

    


#revisa si la cadena es valida
# for palabra in palabrasPrueba:
#     print(f"La palabra es: {palabra}")
#     if luces_nfa.accepts_input(palabra):
#         print("La cadena es aceptada")
#     else:
#         print("Cadena no aceptada")

#dice el estado final
# estados_finales = luces_nfa.read_input('ebzpb')
# print(estados_finales)

# #permite ver todos los caminos cuando estamos en alguna estado
# transiciones_q0 = luces_nfa.transitions.get('q5', {})

# for simbolo, destinos in transiciones_q0.items():
#     print(f"Símbolo '{simbolo}' te lleva a -> {destinos}")

# #Revisa todas las posibilidades a medida que se avanza con la cadena
# for paso, estados in enumerate(luces_nfa.read_input_stepwise('ebzpb')):
#     print(f"Paso {paso}: {estados}")


