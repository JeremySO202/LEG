#mov

class Mov:
    def __init__(self, _destino, _fuente, _procesador):
        self.destino = _destino
        self.fuente = _fuente
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registro fuente R{self.fuente}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.fuente]
        print(f" Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, 0, 0)
        print(f" Valor en ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        self.procesador.regDM.data = self.procesador.regALU.data
        print(f" Valor: {self.procesador.regDM.data}")
    
    def writeback(self):
        print(f"Escribiendo en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Mov.")






