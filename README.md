# Trabajo Práctico: Control de Iluminación Inteligente con Autómatas(FTI)

Proyecto desarrollado para la cátedra **Fundamentos Teóricos de Informática (FTI)**.

El sistema modela y simula el funcionamiento de una tira de luces LED inteligente mediante la teoría de lenguajes formales y autómatas. El proyecto está construido bajo una arquitectura modular **Modelo-Vista-Controlador (MVC)** e integra **Autómatas Finitos Determinísticos (AFD)**, **Máquinas de Moore** y un **Autómata de Pila** para la gestión de historial y retroceso ("deshacer").

---

## Integrantes

* **Lucas Ruiz**
* **Jordan Sandoval Molina**
* **Matias Segurado**

---

## Novedades y Actualizaciones Recientes

* **Arquitectura Modelo-Vista-Controlador (MVC):** Desacoplamiento total entre la lógica formal de los autómatas (`Modelo/`), la interfaz gráfica interactiva (`Vista/`) y la orquestación de eventos (`Controlador/`).
* **Autómata de Pila (`AutomataDePila` / Deshacer):** Implementación de una memoria de pila para almacenar estados previos y permitir la función de **retroceso / deshacer (`d`)** en la tira de luces.
* **Autómata de Control de Brillo (`Brillo`):** Máquina de Moore independiente para gestionar 5 niveles de intensidad luminosa (`1` a `5`).
* **Control Multicanal de Focos:** Simulación de una tira LED de múltiples focos sincronizados.
* **Interfaz Gráfica con Tkinter:** Tablero interactivo con botones de comando, visualización en vivo de la tira LED, niveles de brillo e indicador de caminos de transición disponibles.

---

## Descripción del Sistema

El sistema simula el funcionamiento de una tira LED inteligente hogareña controlada por eventos/comandos:

* **Encendido y Apagado:** Control general de energía.
* **Colores estáticos:** Blanco, Rojo, Verde y Azul.
* **Modos Intermitentes:** Efecto de parpadeo para cada uno de los colores.
* **Modo Dinámico RGB:** Ciclo secuencial de colores en la tira.
* **Control de Brillo:** Ajuste dinámico de intensidad en 5 niveles.
* **Función Deshacer (Pila):** Capacidad de volver al estado anterior en el historial de navegación.

---

### 1. Autómata de Estados del Foco (`Foco` - DFA + Máquina de Moore + Pila)

Modela los modos de iluminación del foco y hereda capacidades de pila para recordar el historial de estados:

#### Conjunto de Estados ($Q$)

* **`q0`**: Apagado (OFF)
* **`q1`**: Blanco estático
* **`q2`**: Rojo estático
* **`q3`**: Verde estático
* **`q4`**: Azul estático
* **`q5`**: Intermitente blanco
* **`q6`**: Intermitente rojo
* **`q7`**: Intermitente verde
* **`q8`**: Intermitente azul
* **`q9`**: Patrón RGB dinámico
* **`q10`**: Menú de patrones / Transición

* `a`: Apagar
* `b`: Blanco
* `r`: Rojo
* `v`: Verde
* `z`: Azul
* `i`: Activar modo intermitente
* `g`: Activar modo RGB
* `p`: Parada / Menú de patrones
* `d`: Deshacer (retroceso en la pila)

#### Salidas de la Máquina de Moore ($\Delta$)

Cada estado genera un comportamiento visual determinado e independiente del canal de entrada:
$$\lambda(q) \in \{\text{Apagado, Blanco, Rojo, Verde, Azul, Intermitente blanco, Intermitente rojo, Intermitente verde, Intermitente azul, Patron RGB, Menu Patrones}\}$$

#### Comportamiento de Pila ($\Gamma$)

Al realizar una transición válida, el estado actual se apila ($push$). La acción de retroceder ejecuta un desapilado ($pop$), restaurando el estado inmediatamente anterior del sistema.

---

### 2. Autómata de Control de Brillo (`Brillo` - Máquina de Moore)

Controla los niveles de intensidad lumínica:

* **Estados ($Q$):** $\{q_0, q_1, q_2, q_3, q_4\}$
* **Alfabeto de Entrada ($\Sigma$):** $\{1, 2, 3, 4, 5\}$
* **Salidas ($\Delta$):** $\{\text{Bajo}, \text{Tenue}, \text{Medio}, \text{Alto}, \text{Maximo}\}$

---

## Estructura del Proyecto (MVC)

```text
Trabajo-Fti-1/
├── Modelo/
│   ├── MaquinaDeMoore.py       # Clase base para autómatas con salidas
│   ├── AutomataPila.py         # Extensión con memoria de pila (historial/deshacer)
│   ├── foco.py                 # Definición del DFA de iluminación y sus salidas
│   └── brillo.py               # Máquina de Moore para los 5 niveles de brillo
├── Vista/
│   └── vista_tira_led.py       # Interfaz gráfica de usuario con Tkinter
├── Controlador/
│   └── controlador_tira_led.py # Coordinador de la tira LED, animaciones y comandos
├── main.py                     # Punto de entrada principal de la aplicación
├── automata_Proyecto_Grupo8.jff # Modelo del autómata para JFLAP
└── simulador_tira_led_moore.html # Simulador interactivo web
```

---

## Requisitos e Instalación

El proyecto requiere **Python 3.10+**.

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Trabajo-Fti-1
```

### 2. Instalar dependencias

```bash
pip install automata-lib
```

---

## Modos de Ejecución

### 1. Aplicación Principal (Arquitectura MVC + GUI)

Inicia la aplicación completa con la interfaz gráfica en Tkinter:

```bash
python main.py
```

### 2. Simulador Web

Abre directamente en tu navegador preferido el archivo:

```text
simulador_tira_led_moore.html
```

### 3. Simulación y Validación en JFLAP

Puedes abrir el archivo `automata_Proyecto_Grupo8.jff` en **JFLAP** para realizar pruebas de cadenas paso a paso y visualizar la estructura de transiciones.

---

## Diagrama de los Autómata

Grafico del Diagrama actual:
