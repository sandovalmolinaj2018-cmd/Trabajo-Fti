from automata.fa.dfa import DFA
from maquina_moore import MaquinaDeMoore

# 1. Definición matemática del DFA (El Cerebro)
# Volcamos exactamente la tabla de transiciones de tu documento.
# Usamos allow_partial=True para que la librería nos deje omitir las flechas
# inválidas, dejando que la clase MaquinaDeMoore las rechace automáticamente.
dfa_foco = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    input_symbols={'e', 'a', 'b', 'r', 'v', 'z', 'p', 'i', 'g'},
    transitions={
        'q0':  {'e': 'q1'},
        'q1':  {'a': 'q0', 'r': 'q2', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q5', 'g': 'q9'},
        'q2':  {'a': 'q0', 'b': 'q1', 'v': 'q3', 'z': 'q4', 'p': 'q10', 'i': 'q6'},
        'q3':  {'a': 'q0', 'b': 'q1', 'r': 'q2', 'z': 'q4', 'p': 'q10', 'i': 'q7'},
        'q4':  {'a': 'q0', 'b': 'q1', 'r': 'q2', 'v': 'q3', 'p': 'q10', 'i': 'q8'},
        'q5':  {'a': 'q0', 'b': 'q1'},
        'q6':  {'a': 'q0', 'r': 'q2'},
        'q7':  {'a': 'q0', 'v': 'q3'},
        'q8':  {'a': 'q0', 'z': 'q4'},
        'q9':  {'a': 'q0', 'p': 'q10'},
        'q10': {'a': 'q0', 'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'g': 'q9'}
    },
    initial_state='q0',
    final_states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    allow_partial=True  
)

# 2. Diccionario de salidas físicas de Moore (El Traductor)
# Respetamos tus nombres de estados y efectos.
salidas_foco = {
    'q0':  "🔌 APAGADA",
    'q1':  "💡 BLANCA",
    'q2':  "💡 ROJA",
    'q3':  "💡 VERDE",
    'q4':  "💡 AZUL",
    'q5':  "✨ BLANCA INTERMITENTE",
    'q6':  "✨ ROJA INTERMITENTE",
    'q7':  "✨ VERDE INTERMITENTE",
    'q8':  "✨ AZUL INTERMITENTE",
    'q9':  "🌈 PATRÓN RGB / ARCOÍRIS",
    'q10': "⚙️ SELECTOR DE PATRÓN"
}

# 3. Instanciamos la Máquina de Moore conectando ambas piezas
foco_principal = MaquinaDeMoore(dfa_foco, salidas_foco)

# 4. Bucle continuo de interacción
print("--- Sistema de Iluminación Iniciado ---")
print("Estado inicial:", foco_principal.obtener_estado_fisico())
print("Alfabeto:")
print(" e: Encender | a: Apagar   | b: Blanco | r: Rojo | v: Verde | z: Azul")
print(" i: Intermit.| p: Patrones | g: RGB")
print("-" * 45)

<<<<<<< Updated upstream
def caminos_posibles(cadenaActual: str):  
    estado_actual = luces_nfa.read_input(cadenaActual)
    opciones = []

    for estado in estado_actual: ##Obtenemos los nodos a los que podemos ir
        nodo = luces_nfa.transitions.get(estado,"Error")

        for caminos_posibles in nodo.values(): #Obtenemos los caminos de cada nodo y los guardamos en la lista de opciones
            prefijo = frozenset(caminos_posibles)
            opciones.append(prefijo)

    print("Podes cambiar el foco a:")
    for opcion in opciones:  
        print(f"{traducido.get(opcion, "Error")}")


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
salir = salir 
comandos = ver lista de comandos"""


cadenaPalabra = ""
ejecucion = True
print("Bienvenido, te presentamos que significa cada abreviatura: ")
print(comandos)
while ejecucion:

    letraActual = input("Ingrese la letra o comando: ").strip()
    if letraActual != "salir" and letraActual !="comandos" :
        cadenaPalabra = cadenaPalabra + letraActual   
        print(f"Tu palabra formada por ahora es: {cadenaPalabra}")
        if luces_nfa.accepts_input(cadenaPalabra):
            print(f"La palabra es aceptada, actualmente te encuntras en el estado de: {traduccionEstado(cadenaPalabra)}")
        else:
            print(f"La palabra fue rechazada")
            cadenaPalabra = cadenaPalabra[:-len(letraActual)] 
            caminos_posibles(cadenaPalabra)  
=======
while True:
    comando = input("\nIngresá un comando (o 'salir' para terminar): ").strip().lower()
    
    if comando == 'salir':
        print("Apagando el sistema...")
        break
        
    if len(comando) != 1 or comando not in dfa_foco.input_symbols:
        print("⚠️ Comando inválido. Usá solo letras del alfabeto.")
        continue
        
    fue_aceptado, salida_actual = foco_principal.procesar_comando(comando)
    
    if fue_aceptado:
        print(f"✅ Transición exitosa -> {salida_actual}")
>>>>>>> Stashed changes
    else:
        print(f"❌ Comando ignorado. El foco sigue: {salida_actual}")