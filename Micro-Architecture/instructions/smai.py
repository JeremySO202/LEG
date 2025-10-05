# suma con inmediato
class Smai:
    def __init__(self, _destino, _registro1, _inmediate, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.inmediate = _inmediate
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registro R{self.registro1}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro1]
        print(f"Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Sumando registro + inmediato ({self.inmediate})")
        if self.procesador.regRF.data is None:
            raise ValueError(f"el Reg {self.registro1} es None y no puede sumarse.")
        self.procesador.regALU.data = self.procesador.ALU.operar(
            self.procesador.regRF.data, self.inmediate, 0 )
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para SmaI")
        self.procesador.regDM.data = self.procesador.regALU.data
    
    def writeback(self):
        print(f"Escribiendo resultado en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Smai.")