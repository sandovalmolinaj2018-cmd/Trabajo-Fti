import time
import threading
from flask import Flask, render_template, jsonify, request
from Controlador.controlador_tira_led_css import ControladorTiraLedCss

app = Flask(__name__)
controlador = ControladorTiraLedCss()

# Bucle en segundo plano para manejar las animaciones (intermitentes / RGB)
def bucle_animacion():
    while True:
        time.sleep(controlador.intervalo_ms / 1000.0)
        controlador.avanzar_animacion()

# Iniciar hilo de animación
hilo = threading.Thread(target=bucle_animacion, daemon=True)
hilo.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/estado')
def obtener_estado():
    return jsonify({
        "colores": controlador.colores_ultimos,
        "brillo": controlador.brillo_actual
    })

@app.route('/api/comando', methods=['POST'])
def enviar_comando():
    data = request.get_json()
    comando = data.get('comando')
    controlador.procesar_comando(comando)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    controlador.actualizar_pantalla()
    app.run(debug=True, port=5000)