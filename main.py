import tkinter as tk
from Vista.vista_tira_led import VistaTiraLed
from Controlador.controlador_tira_led import ControladorTiraLed

def main():
    root = tk.Tk()
    vista = VistaTiraLed(root)
    controlador = ControladorTiraLed(vista)
    controlador.iniciar()
    root.mainloop()

if __name__ == "__main__":
    main()