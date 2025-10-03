#modulo de primos
class MODP:
    def __init__(self, _destino, _registro1, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.prime = 0xFFFFFFFB 
        self.procesador = _procesador

        self.ejecucion = [self.instruccion1, self.instruccion2, self.instruccion3]

    # decode
    def instruccion1(self):
        print("Obteniendo de registro "+str(self.registro1))
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.prime
        print(self.procesador.regRF.data)

    #execute
    def instruccion2(self):
        print("Operando registro")
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data[0], self.procesador.regRF.data[1], 9)
        print(self.procesador.regALU.data)
        
    #write back
    def instruccion3(self):
        print("Guardando resultado en registros")
        self.procesador.RF.registros[self.destino] = self.procesador.regALU.data
        print(str(self.procesador.RF.registros[self.destino]) + " en: " + str(self.destino))

    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en MODP.")