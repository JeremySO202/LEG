#suma
class Add:
    def __init__(self, _destino, _registro1, _registro2, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.procesador = _procesador

        self.ejecucion = [self.etapa1, self.etapa2, self.etapa3]

    def etapa1(self):
        print("Obteniendo de registros "+str(self.registro1)+" y " + str(self.registro2))
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(self.procesador.regRF.data)

    def etapa2(self):
        print("Sumando registros")
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data[0], self.procesador.regRF.data[1], 0)
        print(self.procesador.regALU.data)

    def etapa3(self):
        print("Guardando resultado en registros")
        self.procesador.RF.registros[self.destino] = self.procesador.regALU.data
        print(str(self.procesador.RF.registros[self.destino]) + " en: " + str(self.destino))

       
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Add.")
