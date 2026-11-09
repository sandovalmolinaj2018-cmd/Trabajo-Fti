from Modelo.foco import Foco
from Modelo.brillo import Brillo

class ControladorTiraLed:
    def __init__(self, vista):
        self.vista = vista
        self.vista.set_controlador(self)

        #Creacion tira led
        self.cantidad_focos = 5
        self.tira_focos = []
        for i in range(self.cantidad_focos):
            self.tira_focos.append(Foco())
            
        self.control_brillo = Brillo()
        
        # Traduccion entre el modelo y la vista
        self.colores_tk = {
            "Apagado": "black",
            "Blanco": "white",
            "Rojo": "red",
            "Verde": "green",
            "Azul": "blue",
            "Intermitente blanco": "lightgray",
            "Intermitente rojo": "pink",
            "Intermitente verde": "lightgreen",
            "Intermitente azul": "lightblue",
            "Patron RGB": "magenta",
            "Menu Patrones": "yellow"
        }

    def iniciar(self):
        self.vista.dibujar_tira(self.cantidad_focos)
        self.actualizar_pantalla()

    def procesar_comando(self, comando):
        numeros_brillo = ['1', '2', '3', '4', '5']
        
        if comando in numeros_brillo:
            self.control_brillo.procesar_entrada(comando)
            print(f"Brillo ajustado a: {self.control_brillo.obtener_estado_actual()}")
        else:
            for foco in self.tira_focos:
                foco.procesar_entrada(comando)
            print(f"Color cambiado a: {self.tira_focos[0].obtener_estado_actual()}")

        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        colores_para_pintar = []
        
        for foco in self.tira_focos:
            estado_texto = foco.obtener_estado_actual()
            color_foco = self.colores_tk.get(estado_texto, "black")
            colores_para_pintar.append(color_foco)

        estado_brillo = self.control_brillo.obtener_estado_actual()

        self.vista.actualizar_luces(colores_para_pintar, estado_brillo)