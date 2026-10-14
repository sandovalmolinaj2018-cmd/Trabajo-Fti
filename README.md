# Trabajo Práctico: Control de Iluminación Inteligente con Autómatas (FTI)

Proyecto desarrollado para la materia **Fundamentos Teóricos de Informática (FTI)**. Consiste en la implementación de un **Autómata Finito No Determinístico (AFND)** en Python utilizando la librería `automata-lib` para modelar y controlar el sistema de iluminación inteligente de un hogar.

---

## 👥 Integrantes

* Lucas Ruiz
* Jordan Sandoval Molina
* Matias Segurado

---

## 💡 Descripción del Problema

El objetivo de este proyecto es simular mediante autómatas el funcionamiento de una aplicación móvil de control de iluminación LED hogareña. El usuario puede interactuar con el sistema mediante comandos para:
* Encender y apagar las luces.
* Cambiar entre diferentes colores estáticos (Blanco, Rojo, Verde, Azul).
* Activar modos intermitentes para cada color.
* Seleccionar patrones dinámicos de iluminación (como el modo RGB / Arcoíris).

---

## 🛠️ Requisitos e Instalación

Este proyecto utiliza la librería [automata-lib](https://caleb531.github.io/automata/) para la definición, validación y representación gráfica de autómatas en Python.

### 1. Clonar el repositorio o descargar los archivos
Asegúrate de tener el archivo `luces.py` en tu directorio de trabajo.

### 2. Instalar la librería principal
Instala la biblioteca base mediante `pip`:
```bash
pip install automata-lib
```

### 3. Instalar dependencias visuales (Opcional)
Para generar y exportar el diagrama gráfico del autómata (`diagrama.png`), es necesario contar con Graphviz en tu sistema y las dependencias de visualización:
```bash
pip install 'automata-lib[visual]'
```

---

## ⚙️ Especificación Formal del Autómata

### 1. Estados ($S$)
El autómata cuenta con 11 estados que representan las diferentes combinaciones de encendido, color y patrones:

| Estado | Significado |
| :---: | :--- |
| **$q_0$** | Apagado (Estado inicial y de aceptación) |
| **$q_1$** | Blanco (Encendido) |
| **$q_2$** | Rojo |
| **$q_3$** | Verde |
| **$q_4$** | Azul |
| **$q_5$** | Intermitente Blanco |
| **$q_6$** | Intermitente Rojo |
| **$q_7$** | Intermitente Verde |
| **$q_8$** | Intermitente Azul |
| **$q_9$** | Patrón RGB / Arcoíris |
| **$q_{10}$** | Menú de Patrones |

### 2. Alfabeto ($\Sigma$)
Los símbolos de entrada válidos que la máquina reconoce corresponden a las acciones del usuario:

* **`e`**: Encender
* **`a`**: Apagar
* **`b`**: Blanco
* **`r`**: Rojo
* **`v`**: Verde
* **`z`**: Azul
* **`p`**: Menú de Patrones
* **`i`**: Intermitente
* **`g`**: RGB

$$\Sigma = \{e, a, b, r, v, z, p, i, g\}$$

---

## 🚀 Uso y Ejecución

Para poner en marcha el simulador interactivo y generar automáticamente el diagrama de transiciones en formato PNG, ejecuta el script principal:

```bash
python luces.py
```

Durante la ejecución, la consola te guiará permitiéndote ingresar letras o comandos de forma secuencial. El programa validará en tiempo real si la cadena de comandos es aceptada por el autómata y te indicará el estado actual del sistema lumínico.

---

## 📊 Diagrama de Transiciones

El script incluye llamadas a la función `show_diagram()` de `automata-lib`, la cual compila el comportamiento del AFND y genera una representación gráfica completa de los estados y sus respectivas transiciones.