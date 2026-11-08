import sys
from automata.fa.dfa import DFA
from MaquinaDeMoore import MaquinaDeMoore

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
        'q5':  {'a': 'q0', 'b': 'q1', 'p': 'q10'},
        'q6':  {'a': 'q0', 'r': 'q2', 'p': 'q10'},
        'q7':  {'a': 'q0', 'v': 'q3', 'p': 'q10'},
        'q8':  {'a': 'q0', 'z': 'q4', 'p': 'q10'},
        'q9':  {'a': 'q0', 'p': 'q10'},
        'q10': {'a': 'q0', 'b': 'q5', 'r': 'q6', 'v': 'q7', 'z': 'q8', 'g': 'q9'}
    },
    initial_state='q0',
    final_states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
    allow_partial=True  
)

# Generación del diagrama visual con automata-lib[visual] y Graphviz
try:
    dfa_foco.show_diagram(path="diagrama.png")
    print("📊 Diagrama exportado exitosamente como 'diagrama.png'.")
except Exception as e:
    print(f"⚠️ No se pudo generar el diagrama visual: {e}")

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

def dibujar_foco_consola(estado):
    """Representación visual reactiva del foco con arte ASCII y colores ANSI."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    PALETAS = {
        'q0':  {"c": "\033[90m", "glow": "\033[90m", "icon": "🔌"},
        'q1':  {"c": "\033[97m", "glow": "\033[93m", "icon": "💡"},
        'q2':  {"c": "\033[91m", "glow": "\033[91m", "icon": "🔴"},
        'q3':  {"c": "\033[92m", "glow": "\033[92m", "icon": "🟢"},
        'q4':  {"c": "\033[94m", "glow": "\033[94m", "icon": "🔵"},
        'q5':  {"c": "\033[97m", "glow": "\033[93m", "icon": "✨"},
        'q6':  {"c": "\033[91m", "glow": "\033[91m", "icon": "✨"},
        'q7':  {"c": "\033[92m", "glow": "\033[92m", "icon": "✨"},
        'q8':  {"c": "\033[94m", "glow": "\033[94m", "icon": "✨"},
        'q9':  {"c": "\033[95m", "glow": "\033[96m", "icon": "🌈"},
        'q10': {"c": "\033[93m", "glow": "\033[33m", "icon": "⚙️"}
    }
    
    info = PALETAS.get(estado, PALETAS['q0'])
    c = info['c']
    g = info['glow']
    
    if estado == 'q0':
        art = f"""{DIM}{c}
       .-------.
     /           \\
    |     OFF     |
     \\           /
       '-------'
         |===|
         \\___/{RESET}"""
    elif estado in ('q5', 'q6', 'q7', 'q8'):
        art = f"""
  {g}⚡   \\   :   /   ⚡{RESET}
    {c} -  .-----.  -{RESET}
  {g}✨  /  {BOLD}{info['icon']}{RESET}{c}   \\  ✨{RESET}
 {g}==== | FLASH | ===={RESET}
  {g}✨  \\  {BOLD}{info['icon']}{RESET}{c}   /  ✨{RESET}
    {c} -  '-----'  -{RESET}
  {g}⚡   /   :   \\   ⚡{RESET}
       {DIM}|===|{RESET}
       {DIM}\\___/{RESET}"""
    elif estado == 'q9':
        art = f"""
  \033[91m\\   \033[93m:   \033[92m/{RESET}
\033[96m-  \033[95m.-----.  \033[91m-{RESET}
\033[93m:  \033[92m/  🌈   \\  \033[96m:{RESET}
\033[95m--- \033[91m| R G B | \033[93m---{RESET}
\033[92m:  \033[96m\\       /  \033[95m:{RESET}
\033[91m-  \033[93m'-----'  \033[92m-{RESET}
  \033[96m/   \033[95m:   \033[91m\\{RESET}
     \033[90m|===|\033[0m
     \033[90m\\___/\033[0m"""
    else:
        art = f"""
    {g}\\   :   /{RESET}
  {g}-  {c}.-----.  {g}-{RESET}
 {g}:  {c}/       \\  {g}:{RESET}
{g}--- {c}|   {BOLD}{info['icon']}{RESET}{c}   | {g}---{RESET}
 {g}:  {c}\\       /  {g}:{RESET}
  {g}-  {c}'-----'  {g}-{RESET}
    {g}/   :   \\{RESET}
       {DIM}|===|{RESET}
       {DIM}\\___/{RESET}"""
    print(art)

def caminos_posibles():  
    transiciones = dfa_foco.transitions.get(foco_principal.estado_actual, {})
    if not transiciones:
        print("No hay transiciones posibles desde este estado.")
        return
    print("\nPodés cambiar el foco a:")
    for simbolo, proximo_estado in transiciones.items():
        salida = salidas_foco.get(proximo_estado, "Desconocido")
        print(f" - [{simbolo}]: {salida} ({proximo_estado})")


comandos = """ 
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

def iniciar_consola():
    cadenaPalabra = ""
    ejecucion = True

    # 4. Bucle continuo de interacción
    print("=" * 50)
    print("💡 --- SISTEMA DE ILUMINACIÓN INTELIGENTE (FTI) ---")
    print("=" * 50)
    print("Estado inicial:", foco_principal.obtener_estado_fisico())
    dibujar_foco_consola(foco_principal.estado_actual)
    print("\nAlfabeto y comandos:")
    print(comandos)
    print("\n💡 TIP: También podés abrir la interfaz gráfica con: python foco_gui.py")
    print("-" * 50)

    while ejecucion:
        letraActual = input("\nIngrese la letra o comando: ").strip().lower()

        if letraActual == "salir":
            ejecucion = False
            print("Apagando el sistema...")
        elif letraActual == "comandos":
            print(comandos)
        elif letraActual == "":
            continue
        elif len(letraActual) == 1:
            if letraActual not in dfa_foco.input_symbols:
                print(f"⚠️ El símbolo '{letraActual}' no pertenece al alfabeto.")
                caminos_posibles()
                continue

            fue_aceptado, salida_actual = foco_principal.procesar_comando(letraActual)
            if fue_aceptado:
                cadenaPalabra += letraActual
                print(f"✅ Transición exitosa -> {salida_actual}")
                print(f"Palabra formada por ahora: '{cadenaPalabra}' (Estado: {foco_principal.estado_actual})")
                dibujar_foco_consola(foco_principal.estado_actual)
            else:
                print(f"❌ La acción '{letraActual}' fue rechazada. El foco sigue: {salida_actual}")
                dibujar_foco_consola(foco_principal.estado_actual)
                caminos_posibles()
        else:
            # Permite secuencias de comandos (ej. 'er', 'ebv', etc.)
            if all(c in dfa_foco.input_symbols for c in letraActual):
                todos_aceptados = True
                for c in letraActual:
                    fue_aceptado, salida_actual = foco_principal.procesar_comando(c)
                    if fue_aceptado:
                        cadenaPalabra += c
                    else:
                        print(f"❌ La acción '{c}' fue rechazada desde el estado {foco_principal.estado_actual}.")
                        todos_aceptados = False
                        break
                if todos_aceptados:
                    print(f"✅ Secuencia aceptada -> {salida_actual}")
                    print(f"Palabra formada por ahora: '{cadenaPalabra}' (Estado: {foco_principal.estado_actual})")
                    dibujar_foco_consola(foco_principal.estado_actual)
                else:
                    print(f"El foco sigue: {salida_actual}")
                    dibujar_foco_consola(foco_principal.estado_actual)
                    caminos_posibles()
            else:
                print("⚠️ Comando desconocido. Escriba 'comandos' para ver las opciones disponibles.")

    print("\n¡Hasta luego!")

if __name__ == "__main__":
    if "--gui" in sys.argv:
        from foco_gui import main as gui_main
        gui_main()
    else:
        iniciar_consola()
