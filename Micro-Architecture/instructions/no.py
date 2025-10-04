#not 

class No:
    def __init__(self, _destino, _registro, _procesador):
        self.destino = _destino
        self.registro = _registro
        self.procesador = _procesador

        self.ejecucion = [self.etapa1, self.etapa2]

    def etapa1(self):
        print(f"Obteniendo valor del registro {self.registro}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro]
        print(f"Valor leído: {self.procesador.regRF.data}")

    def etapa2(self):
        print("Aplicando NO")
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, 0, 7)
        print(f"Resultado: {self.procesador.regALU.data}")

        # Guardar resultado en el registro destino
        self.procesador.RF.registros[self.destino] = self.procesador.regALU.data
        print(f"{self.procesador.RF.registros[self.destino]} guardado en registro {self.destino}")


    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en No.")
