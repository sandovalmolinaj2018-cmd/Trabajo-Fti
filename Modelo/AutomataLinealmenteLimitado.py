class AutomataLinealmenteLimitado:
    Tope_izquierdo = '<'
    Tope_derecho = '>'

    def __init__(self, cantidad, diccionario, valores_iniciales=None, mostrar_mensajes=True):
        self.mostrar_mensajes = mostrar_mensajes
        self.estado_actual = "q_inicio"
        self.cantidad_celdas = cantidad 
        self.mapa_slots = diccionario 
        self.cinta = [self.Tope_izquierdo]

        for i in range(1, self.cantidad_celdas + 1):
            if valores_iniciales is not None and i in valores_iniciales:
                self.cinta.append(valores_iniciales[i])
            else:
                self.cinta.append(None)

        self.cinta.append(self.Tope_derecho)
        self.posicion_cabezal = 1

    def obtener_indice_limite_derecho(self):
        return len(self.cinta) - 1

    def mover_cabezal(self, direccion):
        if direccion == 'D':
            siguiente_indice = self.posicion_cabezal + 1
            if self.cinta[siguiente_indice] != self.Tope_derecho:
                self.posicion_cabezal = siguiente_indice
                if self.mostrar_mensajes == True:
                    print("Cabezal movido a la derecha, estas en la Celda " + str(self.posicion_cabezal))
            else:
                if self.mostrar_mensajes == True:
                    print("No te puede mover a la derecha porque llegaste al limite")

        elif direccion == 'I':
            anterior_indice = self.posicion_cabezal - 1
            if self.cinta[anterior_indice] != self.Tope_izquierdo:
                self.posicion_cabezal = anterior_indice
                if self.mostrar_mensajes == True:
                    print("Cabezal movido a la izquierda, estas en la Celda  " + str(self.posicion_cabezal))
            else:
                if self.mostrar_mensajes == True:
                    print("No te puede mover a la izquierda porque llegaste al limite")

        elif direccion == 'N':
            if self.mostrar_mensajes == True:
                print("No te moviste, estas en la celda" + str(self.posicion_cabezal))

    def posicionar_cabezal(self, indice_objetivo):
        indice_maximo = self.obtener_indice_limite_derecho()
        if indice_objetivo <= 0 or indice_objetivo >= indice_maximo:
            return False
        self.estado_actual = 'q_buscando'

        while self.posicion_cabezal != indice_objetivo:
            if self.posicion_cabezal < indice_objetivo:
                self.mover_cabezal('D')
            else:
                self.mover_cabezal('I')

        self.mover_cabezal('N')
        return True

    def escribir_en_slot(self, identificador_slot, datos):
        if identificador_slot not in self.mapa_slots:
            return False
        indice_celda = self.mapa_slots[identificador_slot]
        exito = self.posicionar_cabezal(indice_celda)

        if exito == False:
            return False
        self.cinta[self.posicion_cabezal] = datos

        if self.mostrar_mensajes == True:
            print("Celda " + str(self.posicion_cabezal) + " actualizada" )
        return True

    def leer_desde_slot(self, identificador_slot):
        if identificador_slot not in self.mapa_slots:
            return None

        indice_celda = self.mapa_slots[identificador_slot]
        exito = self.posicionar_cabezal(indice_celda)

        if exito == False:
            return None

        self.estado_actual = 'q_leyendo'
        datos_leidos = self.cinta[self.posicion_cabezal]
        self.estado_actual = 'q_reposo'

        if self.mostrar_mensajes == True:
            print("Celda: " + str(self.posicion_cabezal) + " leida")

        return datos_leidos

    def obtener_etiqueta_celda(self, indice_celda, contenido):
        if contenido is None:
            return "Celda_" + str(indice_celda) + " esta vacia"
        else:
            return "Celda_" + str(indice_celda) + ":" + str(contenido)

    def ver_cinta(self):
        texto_final = ""
        
        for i in range(len(self.cinta)):
            if i == 0:
                valor_celda = self.Tope_izquierdo
            elif i == (len(self.cinta) - 1):
                valor_celda = self.Tope_derecho
            else:
                contenido = self.cinta[i]
                if contenido is None:
                    valor_celda = "Vacio"
                else:
                    valor_celda = str(contenido)

            if i == self.posicion_cabezal:
                valor_celda = valor_celda + " Aca esta el cabezal"
                
            if i == 0:
                texto_final = valor_celda
            else:
                texto_final = texto_final + " | " + valor_celda
                
        return texto_final