# Sistema de Control de Tira LED mediante Autómatas Formales (`Trabajo-Fti`)

Aplicación de escritorio desarrollada en Python para la simulación y el control de una tira de luces LED inteligente, modelada íntegramente mediante la composición de tres máquinas abstractas de la jerarquía de Chomsky: un **Autómata de Moore**, un **Autómata de Pila Determinista (DPDA)** y un **Autómata Linealmente Acotado (ALL)**.

* **Institución:** Universidad Nacional de la Patagonia San Juan Bosco (UNPSJB) – Facultad de Ingeniería
* **Cátedra:** Fundamentos Teóricos de Informática (FTI)
* **Repositorio:** [github.com/sandovalmolinaj2018-cmd/Trabajo-Fti](https://github.com/sandovalmolinaj2018-cmd/Trabajo-Fti.git)

---

## 1. Arquitectura y Fundamentación Teórica

El sistema desacopla el control operativo de la tira LED en tres niveles de capacidad computacional, evitando la explosión combinatoria de estados que ocurriría al intentar modelar memoria e historial únicamente con autómatas finitos.

### A. Autómata de Moore (Control Base, Color e Intensidad)
Gestiona los estados físicos inmediatos del dispositivo (encendido/apagado, selección de color base y regulación de intensidad lumínica). Al tratarse de una máquina de Moore, la salida emitida hacia la interfaz/hardware depende **exclusivamente del estado actual** y no de la transición entrante.

* **Definición formal:** $M_{Moore} = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$
  * **Niveles de brillo ($\Delta_{brillo}$):** `{"Muy bajo", "Bajo", "Medio", "Alto", "Máximo"}`
  * **Función de salida ($\lambda: Q \rightarrow \Delta$):** Determina el estado visual activo del foco/tira LED (`obtener_salida_actual()`).

### B. Autómata de Pila Determinista – DPDA (Historial y Función Deshacer)
Permite almacenar cronológicamente las configuraciones de color y estado aplicadas por el usuario, habilitando la reversión secuencial de cambios (*Undo* / `retroceder`) sin perder el contexto previo.

* **Definición formal:** $M_{DPDA} = (Q, \Sigma, \Gamma, \delta, q_0, Z, F)$
  * **Alfabeto de pila ($\Gamma$):** `{Z, C_1, C_2, ..., C_n}`, donde `Z` actúa como marca de fondo de pila (`[DEF]`).
  * **Criterio de aceptación:** Por pila vacía / retorno al estado base sobre `Z`.

| Operación | Símbolo de Entrada | Tope de Pila | Acción en Pila | Efecto en el Sistema |
| :--- | :---: | :---: | :---: | :--- |
| **Aplicar color / estado** | `c_i` | `X` | `PUSH(c_i)` sobre `X` | Actualiza la tira LED y guarda el estado en el historial. |
| **Deshacer (`retroceder`)** | `'d'` | `c_i` ($\neq$ `Z`) | `POP` | Elimina el estado actual y restaura el color anterior en el tope. |
| **Deshacer en base** | `'d'` | `Z` | Mantener `Z` | Mantiene el estado por defecto `[DEF]` sin desbordar la pila. |

### C. Autómata Linealmente Acotado – ALL (Gestión de Presets en Memoria)
Implementa una cinta finita acotada proporcionalmente al tamaño de la entrada para almacenar, recorrer y sobreescribir perfiles de iluminación predefinidos (*presets* de usuario) mediante un cabezal de lectura/escritura bidireccional.

* **Definición formal:** $M_{ALL} = (Q, \Sigma, \Gamma, \delta, q_0, \triangleleft, \triangleright, F)$
  * **Estructura de la cinta:** `['<', DEF, P1, P2, P3, '>']`
  * **Marcadores de frontera:** `'<'` (límite izquierdo, $\triangleleft$) y `'>'` (límite derecho, $\triangleright$), que impiden que el cabezal salga del espacio asignado.
  * **Movimientos del cabezal:** `I` (Izquierda), `D` (Derecha), `N` (Neutro / Lectura-Escritura en celda activa).

---

## 2. Estructura del Proyecto

```text
Trabajo-Fti/
├── models/                      # Modelos formales diseñados y validados en JFLAP
│   └── Aut-Foco-PDA.jff         # Definición XML del Autómata de Pila Determinista
├── src/                         # Código fuente principal (o raíz según rama activa)
│   ├── main.py                  # Punto de entrada de la aplicación e interfaz gráfica
│   ├── AutomataPila.py          # Implementación formal del DPDA y gestión de pila
│   ├── Foco.py                  # Modelo de estados de salida (Autómata de Moore)
│   ├── controlador_tira_led.py  # Orquestador entre la vista, el DPDA, Moore y el ALL
│   └── ...                      # Implementación de la cinta acotada (ALL) y utilidades
├── docs/                        # Diagramas de transición, informes y documentación teórica
├── requirements.txt             # Dependencias de Python del proyecto
└── README.md                    # Documentación técnica del repositorio
```

---

## 3. Requisitos e Instalación

### Prerrequisitos del Sistema Operativo
Antes de instalar los paquetes de Python, asegurate de contar con **Graphviz** (necesario para renderizar diagramas de estados con `automata-lib`) y **Tkinter** (interfaz gráfica):

* **Ubuntu / Debian:**
  ```bash
  sudo apt update
  sudo apt install -y python3-venv python3-tk graphviz graphviz-dev pkg-config
  ```
* **Windows 10 / 11:**
  1. Instalar Python 3.10+ marcando *"Add Python to PATH"*.
  2. Instalar [Graphviz para Windows](https://graphviz.org/download/) y seleccionar *"Add Graphviz to the system PATH for all users"*.

### Configuración del Entorno Virtual

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/sandovalmolinaj2018-cmd/Trabajo-Fti.git](https://github.com/sandovalmolinaj2018-cmd/Trabajo-Fti.git)
   cd Trabajo-Fti
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv .venv
   # En Linux / macOS:
   source .venv/bin/activate
   # En Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install --default-timeout=100 -r requirements.txt
   ```

---

## 4. Uso y Ejecución

Con el entorno virtual activado, iniciá el panel de control de la tira LED ejecutando:

```bash
python main.py
```

### Flujo de Interacción en la Interfaz
1. **Encendido y Selección de Color (Moore + DPDA):** Al seleccionar un color o intensidad, el Autómata de Moore actualiza la salida visual y el DPDA apila la nueva configuración sobre la pila.
2. **Reversión de Estado (DPDA):** Al presionar el botón **Deshacer / Retroceder** (entrada `'d'`), el sistema ejecuta `POP` y recupera el estado inmediato anterior hasta alcanzar `[DEF]`.
3. **Navegación de Presets (ALL):** Mediante los controles de desplazamiento (`I` / `D`), el cabezal recorre las ranuras `DEF`, `P1`, `P2` y `P3` respetando los topes `'<'` y `'>'` para cargar o guardar escenas.

---

## 5. Equipo de Desarrollo

* **Jordan David Sandoval Molina**
* **Lucas Ruiz**
* **Matias Segurado**
