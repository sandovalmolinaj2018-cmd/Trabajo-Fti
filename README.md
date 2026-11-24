# Sistema de Control de Iluminación LED

Trabajo integrador de Fundamentos Teóricos de Informática.

App de escritorio hecha en Python con Tkinter que simula una tira de 5 focos LED. Que se maneja mediante comandos (encender, apagar, colores, intermitente, patrones, brillo y deshacer) y permite guardar y cargar configuraciones a gusto del usuario. Todo el comportamiento está modelado con autómatas.

## Armado

Son tres modelos que trabajan juntos:

**Foco** - `Modelo/foco.py` y `Modelo/AutomataPila.py`

Tiene 11 estados: apagado, blanco, rojo, verde, azul, los cuatro intermitentes, patrón RGB y menú de patrones. La salida depende solo del estado en el que está. Además tiene una pila que sirve para dos cosas, deshacer y recordar qué estado estaba antes de apagarse. Cada vez que cambia de estado apila el símbolo del estado anterior, y con `d` lo desapila para volver al anterior estado. Hay un autómata por cada foco y los 5 reciben los mismos comandos.

**Brillo** - `Modelo/brillo.py`

Cinco estados: Bajo (20%), Tenue (40%), Medio (60%), Alto (80%) y Máximo (100%). Arranca en Máximo. Apretar 1, 2, 3, 4 o 5 manda directo al nivel correspondiente. Va separado del foco para no tener que armar un solo autómata de 55 estados.

**Presets** - `Modelo/presets.py` y `Modelo/AutomataLinealmenteLimitado.py`

La cinta es `< DEF | P1 | P2 | P3 >`. El cabezal se mueve a izquierda, derecha o se queda quieto, y los topes `<` y `>` no lo dejan salir. Cada celda guarda un preset: la cadena de comandos que arma ese color, el brillo y los nombres para mostrar. Al cargar un preset, esa cadena se le pasa al autómata del foco como entrada.

| Modelo | Nivel en la jerarquía de Chomsky |
| :--- | :--- |
| Moore (brillo, salida del foco) | Tipo 3 |
| Autómata de pila (foco) | Tipo 2 |
| Autómata linealmente limitado (presets) | Tipo 1 |

Para definir y validar los autómatas se utilizo `automata-lib`, pero la ejecución paso a paso, con la pila y las salidas, la hicimos nosotros en `AutomataPila.py` y `MaquinaDeMoore.py`.

## Comandos

| Comando | Qué hace |
| :---: | :--- |
| `e` | Encender  |
| `a` | Apagar |
| `b` `r` `v` `z` | Blanco, rojo, verde, azul |
| `i` | Intermitente sobre el color actual |
| `p` | Menú de patrones |
| `g` | Patrón RGB (desde el menú) |
| `d` | Deshacer |
| `1` a `5` | Nivel de brillo |

Dentro del menú de patrones se puede ingresar, `b`, `r`, `v` y `z` eligen el color intermitente.

## Requisitos e instalación

Hace falta Python 3.10 o superior y Tkinter. En Windows Tkinter suele venir con Python. En Ubuntu o Debian:

```bash
sudo apt install python3-venv python3-tk
```

Después:

```bash
git clone https://github.com/sandovalmolinaj2018-cmd/Trabajo-Fti.git
cd Trabajo-Fti
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Instalar la libreria y ejecutar:

```bash
pip install automata-lib
python main.py
```

## Cómo se usa

1. Al abrir la app la tira está apagada. Apretá **Encender (e)**.
2. Elegí colores, intermitente, patrones o el nivel de brillo con los botones.
3. **Deshacer (d)** vuelve al estado anterior, paso por paso.
4. En el panel de presets, **Guardar** deja la configuración actual en ese slot y el botón grande de cada slot la carga.

Los presets se guardan en un archivo `presets.json` en la carpeta desde donde se ejecuta el programa.

## Aclaraciones

- Deshacer solo afecta colores y modos, el brillo no se deshace.
- Cargar un preset borra el historial de deshacer.
- El slot DEF se usa en el primer encendido de cada ejecución. Después de apagar y encender, la tira vuelve a lo que estaba antes de apagarse.
- No se puede guardar un preset con la tira apagada, ni cargarlo.
- El ALL tiene 4 celdas fijas. 

## Estructura del proyecto

```text
Trabajo-Fti/
├── Modelo/
│   ├── AutomataPila.py                  # DPDA: pila, transiciones y salida
│   ├── AutomataLinealmenteLimitado.py   # ALL: cinta, cabezal, leer y escribir
│   ├── MaquinaDeMoore.py                # Máquina de Moore
│   ├── foco.py                          # Autómata del foco
│   ├── brillo.py                        # Autómata del brillo 
│   └── presets.py                       # Memoria de presets 
├── Vista/
│   └── vista_tira_led.py                # Interfaz Tkinter
├── Controlador/
│   └── controlador_tira_led.py          # Conecta la vista con los autómatas
├── JFLAP/                               # Modelos hechos en JFLAP
├── main.py                              # Punto de entrada
└── README.md
```

## Equipo

- Jordan David Sandoval Molina
- Lucas Ruiz
- Matias Segurado